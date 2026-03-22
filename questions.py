QUESTION_BANKS = {
    "A": {
        1: {
            "type": "password",
            "story": "Inspector Virkar ne crime scene pe ek torn notebook page dhoondha. Teen words likhe the — lekin seedha nahi, ulta. Har clue ek famous Bollywood fact ki taraf point karta hai. Unhe sahi order mein jodo.",
            "hints": [
                "Clue 1: Shah Rukh Khan ne apni pehli film mein ek villain play kiya tha. Woh film kaunsi thi? Uska LAST word answer ka pehla part hai. → Film: Deewana",
                "Clue 2: 'Gangs of Wasseypur' mein Manoj Bajpayee ke character ka surname kya tha? Yeh answer ka doosra part hai. → KHAN",
                "Clue 3: 'Andhadhun' mein blind pianist ka naam kya tha? Sirf first name chahiye. → AKASH"
            ],
            "question": "Teeno clues combine karke password banao (no spaces, exact case as hinted).",
            "answer": "DeewanaKhanAkash"
        },
        2: {
            "type": "hidden",
            "story": "Ek anonymous tip aaya police ko — ek food blogger ke purane post mein kuch hidden tha. Jo dikhta hai woh sach nahi, jo nahi dikhta woh sach hai.",
            "visible_text": """🍽️ "Mumbai ke best street foods" — A Foodie's Journey

Vada Pav, Pav Bhaji, Bhel Puri... Mumbai ka khana waise hi famous
hai jaise yahan ki film industry. Aaj main aapko bata raha hoon
mere favorite spots ke baare mein.

Bandra mein ek chota sa stall hai jahan ki Misal Pav kamaal ki
hai. Phir Juhu beach pe toh Pani Puri ka mazaa hi alag hai.
Andheri mein ek place hai jahan ceiling pe...""",
            "hidden_text": "WAZIR",
            "question": "Is page mein kuch chhupa hua hai. Dhundho aur likho.",
            "answer": "wazir"
        },
        3: {
            "type": "chat",
            "story": "Do college friends WhatsApp pe ek mystery solve karne ki koshish kar rahe hain.",
            "messages": [
                {"from": "Rohan", "text": "Okay riddle — 2016 film, Dangal ke PEHLE Aamir Khan ki last release. Director wahi jisne TAARE ZAMEEN PAR banaya tha."},
                {"from": "Simran", "text": "Yaar Taare Zameen Par ka director... Aamir ne produce kiya tha. Actually direct kiya tha Amole Gupte ne pehle phir..."},
                {"from": "Rohan", "text": "BHAI. Seedha batao 😂"},
                {"from": "Rohan", "text": "OK FINAL HINT: Film mein Aamir ek coach bana tha real life wrestlers ki — unki daughters ki."},
                {"from": "Simran", "text": "Ohhh GOT IT!! 🎬"},
            ],
            "question": "Is chat mein ultimate mein jis film ki baat ho rahi hai uska naam kya hai?",
            "answer": "dangal"
        },
        4: {
            "type": "meme",
            "meme_top": "Jab tune 5 saal mein complete kiya woh cheez jo logon ne 2 mein ki",
            "meme_emoji": "😤",
            "meme_bottom": "Isko kehte hain...",
            "hidden_tag": "BAAZIGAR",
            "hint_text": "Woh film ek psychological thriller thi jisme hero ne apni hi heroine ko ek iconic scene mein gira diya tha — tabhi audience shocked ho gayi thi.",
            "question": "Yeh meme ek Bollywood film ki taraf hint kar raha hai. Meme mein chhupa hua film ka naam dhundho.",
            "answer": "baazigar"
        },
        5: {
            "type": "riddle",
            "story": "Detective ka aakhri challenge. Teen clues ek famous Bollywood villain ka FULL NAME complete karte hain.",
            "clues": [
                "Clue 1: Is villain ka pehla naam ek sound hai jo darr ko represent karta hai — 6 letters.",
                "Clue 2: Doosra naam India ka sabse common surname — 5 letters.",
                "Clue 3: Is villain ko play karne wale actor ka real naam 'Amjad Khan' tha — confirm karo ki yeh sahi villain hai.",
            ],
            "question": "Villain ka FULL NAME kya hai? (First + Last, space ke saath)",
            "answer": "gabbar singh"
        }
    },
    "B": {
        1: {
            "type": "password",
            "story": "Ek encrypted locker mila — 3 part code hai. Har part ek famous Bollywood moment se nikalta hai.",
            "hints": [
                "Clue 1: 'Dil Se' film mein Shah Rukh Khan ka character ek radio journalist tha. Uska character FIRST NAME kya tha? Yeh pehla part hai. → AMAR",
                "Clue 2: 'Gangs of Wasseypur Part 2' mein Nawazuddin Siddiqui ke character ka naam kya tha? Yeh doosra part hai. → FAIZAL",
                "Clue 3: 'Black Friday' (2004) mein Kay Kay Menon ne ek real-life officer ka role play kiya. Uska SURNAME kya tha? Yeh teesra part hai. → MARIA"
            ],
            "question": "Teeno parts combine karo (no spaces).",
            "answer": "AmarFaizalMaria"
        },
        2: {
            "type": "hidden",
            "story": "Ek shayar ka blog mila jisme ek secret message tha apne dost ke liye. Shayari padhte padhte clue dhundho.",
            "visible_text": """✍️ Aaj Ki Shayari — by Roshan Mirza

Zindagi ke is safar mein,
Kuch log milte hain pal bhar ke liye...
Phir bhi unka asar rehta hai,
Dil ke kisi kone mein hamesha.

Woh jo bichhad jaate hain,
Unhe yaad karte hain hum...
Aankhon mein unka chehra,
Aur hothon pe unka naam.

Kabhi kabhi lagta hai jaise,
Waqt ruk gaya ho kahin...""",
            "hidden_text": "HAIDER",
            "question": "Is blog mein ek Bollywood film ka naam chhupa hua hai. Dhundho.",
            "answer": "haider"
        },
        3: {
            "type": "chat",
            "story": "Do dost ek film ke villain ka naam discuss kar rahe hain.",
            "messages": [
                {"from": "Arjun", "text": "Bhai woh film yaad hai jisme SRK tha aur film ka TITLE hi villain ke naam se related tha?"},
                {"from": "Kabir", "text": "War? Nahi woh alag tha..."},
                {"from": "Arjun", "text": "Nahi! Sci-fi wali. SRK ne villain bhi play kiya tha khud."},
                {"from": "Kabir", "text": "Ohhhh! Woh jisme G.One tha! Toh villain ka naam..."},
                {"from": "Arjun", "text": "Haan! Film ka TITLE = villain ka NAAM. Wahi answer hai."},
            ],
            "question": "Is film ka naam kya tha (jo villain ka naam bhi tha)?",
            "answer": "raone"
        },
        4: {
            "type": "meme",
            "meme_top": "Normal log jo seedha Google pe dhundhte hain",
            "meme_emoji": "😤",
            "meme_bottom": "Main jo pehle Wikipedia, phir IMDb, phir 3 Reddit threads padh ke dhundhta hoon",
            "hidden_tag": "DRISHYAM",
            "hint_text": "Film ek aadmi ke baare mein thi jo apni family ko bachane ke liye ek perfect alibi create karta hai.",
            "question": "Meme mein ek Bollywood film chhupa hua hai — woh film dhundho.",
            "answer": "drishyam"
        },
        5: {
            "type": "riddle",
            "story": "Multi-step riddle. Ek famous Bollywood film aur uske director ko identify karo.",
            "clues": [
                "Clue 1: 2001 ki ek film thi jisme teen dost the — film ka naam do words mein tha. Pehla word ek feeling hai, doosra word ek wish/desire. Film ka naam?",
                "Clue 2: Is film ke director ka SURNAME kya tha? Woh baad mein 'Made in Heaven' web series bhi banayenge.",
                "Clue 3: Wahi surname answer hai — sirf surname likhna hai.",
            ],
            "question": "'Dil Chahta Hai' ke director ka surname kya tha?",
            "answer": "akhtar"
        }
    },
    "C": {
        1: {
            "type": "password",
            "story": "Teen alag films ke teen alag dialogues diye gaye hain — lekin dialogues mein ek word BLANK hai. Teeno blanks milke password banate hain.",
            "hints": [
                "Clue 1: 'Mughal-E-Azam' ka famous dialogue: 'Pyaar kiya toh _______ kya?' → Blank word = DARNA",
                "Clue 2: 'Sholay' ka famous dialogue: 'Kitne aadmi _______?' → Blank word = THE",
                "Clue 3: 'Agneepath' (1990): 'Vijay Deenanath Chauhan. Poora naam. _______ ka naam Deenanath Chauhan.' → Blank word = BAAP"
            ],
            "question": "Teeno blank words combine karo (no spaces, exact case as shown).",
            "answer": "DarnaTheBaap"
        },
        2: {
            "type": "hidden",
            "story": "Ek travel blogger ne Rajasthan trip ke baare mein likha. Carefully padhne pe kuch unusual dikhe.",
            "visible_text": """🏜️ My Rajasthan Diaries — Part 3

Jaipur se Jodhpur ka safar waqai khoobsurat hai.
Mehrangarh fort dekh ke dil bhar aata hai.
Blue city ka har gali, har deewar ek kahani
kehti hai. Wahan ke log bhi utne hi warm hain
jitna wahan ka mausam. Pushkar mela agar
sahi time pe dekho toh life mein ek baar
zaroor karna chahiye. Camel safari ka anubhav
toh words mein describe hi nahi hota...""",
            "hidden_text": "TALVAR",
            "question": "Is travel blog mein ek Bollywood thriller ka naam chhupa hai — woh film ek real-life murder mystery pe based thi. Dhundho.",
            "answer": "talvar"
        },
        3: {
            "type": "chat",
            "story": "Do dost ek Bollywood remake ke baare mein baat kar rahe hain.",
            "messages": [
                {"from": "Meera", "text": "Woh film batao jisme ek police officer apne hi department ke corrupt logon ke khilaf lad raha tha — 2013 ki film, South Indian remake thi, Ajay Devgn tha."},
                {"from": "Dev", "text": "Singham? Nahi woh 2011 tha..."},
                {"from": "Meera", "text": "Nahi! 2013, Rohit Shetty nahi, different director. Telugu remake."},
                {"from": "Dev", "text": "Ram Charan wali ka remake? 'Zanjeer'!"},
                {"from": "Meera", "text": "HAAN! Ab batao — is film mein Ajay Devgn ke character ka naam kya tha? Wahi answer hai."},
            ],
            "question": "Zanjeer (2013) mein Ajay Devgn ke character ka naam kya tha?",
            "answer": "vijay"
        },
        4: {
            "type": "meme",
            "meme_top": "Beta tumse na ho payega",
            "meme_emoji": "😤",
            "meme_bottom": "Jab tune guess kiya film ka naam without dekhe",
            "hidden_tag": "ANDHADHUN",
            "hint_text": "2018 ki National Award winning Bollywood thriller — jisme ek blind pianist tha lekin woh actually blind nahi tha.",
            "question": "Is meme mein ek 2018 ki Bollywood thriller chhupa hua hai. Film ka naam dhundho.",
            "answer": "andhadhun"
        },
        5: {
            "type": "riddle",
            "story": "4 clues. Har clue ek letter deta hai. Phir un letters se ek famous director ka surname banao.",
            "clues": [
                "Letter 1: 'Dil Chahta Hai' ke director ka PEHLA letter → F",
                "Letter 2: 'Zindagi Na Milegi Dobara' ki director ka PEHLA letter → Z",
                "Letter 3: Yeh dono ek hi family se hain. Unke FATHER ka naam? Pehla letter → J",
                "Letter 4: Yeh poori family ek SURNAME share karti hai — wahi answer hai.",
            ],
            "question": "Farhan, Zoya, aur Javed — teeno ka shared surname kya hai?",
            "answer": "akhtar"
        }
    }
}
