document.addEventListener('DOMContentLoaded', () => {
    // 1. Hero Canvas Particles
    const canvas = document.getElementById('hero-canvas');
    if (canvas) {
        const ctx = canvas.getContext('2d');
        let width = canvas.width = window.innerWidth;
        let height = canvas.height = window.innerHeight;
        
        const particles = [];
        for(let i=0; i<50; i++) {
            particles.push({
                x: Math.random() * width,
                y: Math.random() * height,
                vx: (Math.random() - 0.5) * 0.5,
                vy: (Math.random() - 0.5) * 0.5,
                r: Math.random() * 2 + 0.5
            });
        }
        
        function draw() {
            ctx.clearRect(0, 0, width, height);
            ctx.fillStyle = 'rgba(255, 184, 0, 0.3)';
            for(let i=0; i<particles.length; i++) {
                let p = particles[i];
                ctx.beginPath();
                ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
                ctx.fill();
                p.x += p.vx;
                p.y += p.vy;
                if(p.x < 0) p.x = width;
                if(p.x > width) p.x = 0;
                if(p.y < 0) p.y = height;
                if(p.y > height) p.y = 0;
            }
            requestAnimationFrame(draw);
        }
        draw();
        
        window.addEventListener('resize', () => {
            width = canvas.width = window.innerWidth;
            height = canvas.height = window.innerHeight;
        });
    }

    // 2. Confirm Countdown
    const countdownEl = document.getElementById('countdown');
    const startBtn = document.getElementById('start-btn');
    if (countdownEl && startBtn) {
        let count = parseInt(countdownEl.innerText);
        const interval = setInterval(() => {
            count--;
            if (count > 0) {
                countdownEl.innerText = count;
                // Add tiny shake/pulse effect by reassigning class/animation
                countdownEl.style.animation = 'none';
                countdownEl.offsetHeight; /* trigger reflow */
                countdownEl.style.animation = 'pulse 1s infinite';
            } else {
                clearInterval(interval);
                countdownEl.innerText = "GO!";
                
                // Cinematic flash
                const flash = document.createElement('div');
                flash.style.position = 'fixed';
                flash.style.top = 0; flash.style.left = 0; 
                flash.style.width = '100vw'; flash.style.height = '100vh';
                flash.style.background = '#fff';
                flash.style.zIndex = 10000;
                flash.style.transition = 'opacity 0.5s ease-out';
                document.body.appendChild(flash);
                
                setTimeout(() => {
                    window.location.href = startBtn.href;
                }, 200);
            }
        }, 1000);
    }

    // 3. Level Timer Display
    const timerEl = document.getElementById('timer');
    if (timerEl) {
        const updateTimer = () => {
            fetch('/api/status').then(res => res.json()).then(data => {
                if (data.elapsed_secs !== undefined) {
                    const limitSecs = data.time_limit_secs || 5400;
                    const remaining = limitSecs - data.elapsed_secs;
                    
                    if (remaining <= 0) {
                        window.location.href = '/timeout';
                        return;
                    }
                    
                    const mins = Math.floor(remaining / 60);
                    const secs = remaining % 60;
                    timerEl.innerText = `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;

                    timerEl.className = 'timer-display';
                    if (mins < 2) {
                        timerEl.classList.add('timer-danger');
                    } else if (mins < 10) {
                        timerEl.classList.add('timer-warning');
                    }
                }
            }).catch(e => console.error(e));
        }
        updateTimer();
        setInterval(updateTimer, 1000);
    }

    // 4. Answer Submission (AJAX + Cinematic Effects)
    const answerForm = document.getElementById('answer-form');
    const answerInput = document.getElementById('answer-input');
    const errorMsg = document.getElementById('error-message');
    const successOverlay = document.getElementById('success-overlay');

    if (answerForm) {
        const submitBtn = answerForm.querySelector('button[type="submit"]');

        answerForm.addEventListener('submit', (e) => {
            e.preventDefault();
            if (submitBtn) { submitBtn.disabled = true; submitBtn.textContent = 'CHECKING...'; }
            
            const formData = new FormData(answerForm);
            
            fetch(answerForm.action, {
                method: 'POST',
                body: formData,
                headers: { 'X-CSRFToken': formData.get('csrf_token') }
            })
            .then(res => res.json())
            .then(data => {
                if (data.success && data.redirect) {
                    if (answerInput) answerInput.classList.add('flash-gold');
                    if (successOverlay) successOverlay.classList.add('active');
                    
                    setTimeout(() => { window.location.href = data.redirect; }, 1500);
                } else if (!data.success) {
                    if (data.redirect) {
                        window.location.href = data.redirect;
                    } else {
                        // Wrong answer -> Shake and Toast
                        if (answerInput) {
                            answerInput.classList.remove('shake');
                            void answerInput.offsetWidth; // trigger reflow
                            answerInput.classList.add('shake', 'flash-crimson');
                            setTimeout(() => { answerInput.classList.remove('shake', 'flash-crimson'); }, 500);
                        }
                        
                        if (errorMsg) {
                            errorMsg.innerText = data.message || "Incorrect Answer!";
                            errorMsg.classList.add('toast-visible');
                            setTimeout(() => { errorMsg.classList.remove('toast-visible'); }, 4000);
                        }
                        
                        answerForm.reset();
                        const csrfMeta = document.querySelector('meta[name="csrf-token"]');
                        if (csrfMeta) answerForm.querySelector('input[name="csrf_token"]').value = csrfMeta.getAttribute('content');
                        
                        if (submitBtn) { submitBtn.disabled = false; submitBtn.textContent = 'SUBMIT ANSWER'; }
                    }
                }
            })
            .catch(err => {
                console.error(err);
                if (submitBtn) { submitBtn.disabled = false; submitBtn.textContent = 'SUBMIT ANSWER'; }
            });
        });
    }

    // 5. Leaderboard Polling
    const lbBody = document.getElementById('leaderboard-body');
    const podiumContainer = document.getElementById('podium-container');
    const lastUpdated = document.getElementById('last-updated');
    
    if (lbBody) {
        window.fetchLb = () => {
            fetch('/api/leaderboard').then(res => res.json()).then(data => {
                lbBody.innerHTML = '';
                
                // Podium Logic (Top 3)
                if (podiumContainer && data.length > 0) {
                    const top3 = data.filter(t => t.rank && t.rank !== '-').slice(0, 3);
                    let podiumHTML = '';
                    
                    // Rearrange for podium visual order (2, 1, 3)
                    const ordered = [];
                    if(top3.length > 1) ordered.push({item: top3[1], cls: 'rank-2'});
                    if(top3.length > 0) ordered.push({item: top3[0], cls: 'rank-1'});
                    if(top3.length > 2) ordered.push({item: top3[2], cls: 'rank-3'});
                    
                    ordered.forEach(p => {
                        podiumHTML += `
                            <div class="podium ${p.cls}">
                                <div style="font-size: 1.5rem;">${p.cls === 'rank-1' ? '🥇' : p.cls === 'rank-2' ? '🥈' : '🥉'}</div>
                                <div class="podium-name">${p.item.name}</div>
                                <div class="muted" style="font-size: 0.7rem; margin-top: auto;">${p.item.adjusted_time}s</div>
                            </div>
                        `;
                    });
                    podiumContainer.innerHTML = podiumHTML;
                }
                
                data.forEach(t => {
                    const tr = document.createElement('tr');
                    let statusBadge = '';
                    if (t.status === 'Completed') statusBadge = '<span class="badge badge-gold">✅ SOLVED</span>';
                    else if (t.status === 'Timed Out' || t.status === 'Disqualified') statusBadge = '<span class="badge badge-crimson">⏰ TIME UP</span>';
                    else statusBadge = '<span class="badge badge-cyan">🔍 INVESTIGATING</span>';
                    
                    const rankStr = (t.rank === 1 || t.rank === 2 || t.rank === 3) ? `<span style="color: var(--gold); font-weight: bold;">${t.rank}</span>` : t.rank;
                    const rClass = (t.status === 'Disqualified' || t.status === 'Timed Out') ? 'opacity: 0.5;' : '';

                    tr.innerHTML = `
                        <td style="${rClass}">${rankStr}</td>
                        <td style="font-weight: bold; ${rClass}">${t.name}</td>
                        <td style="${rClass}">${t.levels_completed} / 5</td>
                        <td style="font-family: var(--font-body); ${rClass}">${t.adjusted_time}</td>
                        <td style="${rClass}">${statusBadge}</td>
                    `;
                    lbBody.appendChild(tr);
                });
                
                if (lastUpdated) {
                    const d = new Date();
                    lastUpdated.innerText = "Updated: " + d.toLocaleTimeString();
                }
            });
        };
        window.fetchLb();
        setInterval(window.fetchLb, 30000);
    }
});
