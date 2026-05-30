def is_helper_context(text):
    text_lower = text.lower()

    helper_words = [
        "ik help iemand",
        "ik help een",
        "ik begeleid iemand",
        "ik ondersteun iemand",
        "er is iemand",
        "er is een dakloze",
        "een dakloze",
        "een cliënt",
        "een client",
        "een persoon",
        "iemand heeft",
        "iemand is",
        "dakloze is",
        "dakloze heeft",
        "cliënt heeft",
        "client heeft",
        "persoon heeft"
    ]

    return any(word in text_lower for word in helper_words)


def detect_language(text):
    text_lower = text.lower()

    arabic_chars = any(
        "\u0600" <= char <= "\u06FF"
        for char in text
    )

    polish_chars = any(
        char in text_lower
        for char in ["ą", "ć", "ę", "ł", "ń", "ó", "ś", "ź", "ż"]
    )

    english_words = [
        "where",
        "what",
        "how",
        "help",
        "sleep",
        "shower",
        "hungry",
        "food",
        "documents",
        "insurance",
        "medical",
        "doctor"
    ]

    if arabic_chars:
        return "Arabisch"

    if polish_chars:
        return "Pools"

    english_count = sum(
        word in text_lower
        for word in english_words
    )

    if english_count >= 2:
        return "Engels"

    return "Nederlands"


def is_medical_complaint(text):
    text_lower = text.lower()

    if is_helper_context(text):
        return False

    medical_words = [
        "pijn",
        "borst",
        "bloed",
        "benauwd",
        "flauw",
        "wond",
        "koorts",
        "duizelig",
        "adem",
        "ziek",
        "hoofdpijn",

        "الم",
        "وجع",
        "صداع",
        "مريض",
        "دم",
        "تنفس"
    ]

    return any(
        word in text_lower
        for word in medical_words
    )


def is_medical_care_question(text):
    text_lower = text.lower()

    care_words = [
        "huisarts",
        "dokter",
        "arts",
        "medische hulp",
        "medische zorg",
        "niet verzekerd",
        "geen verzekering",
        "onverzekerd",
        "verzekering",
        "zorg",
        "straatzorg",

        "doctor",
        "medical help",
        "medical care",
        "insurance",
        "not insured",

        "طبيب",
        "تأمين",
        "مساعدة طبية"
    ]

    return any(
        word in text_lower
        for word in care_words
    )


def is_drug_question(text):
    text_lower = text.lower()

    if is_helper_context(text):
        return False

    if is_recovery_question(text):
        return False

    drug_words = [
        "drugs",
        "cocaine",
        "cocaïne",
        "wiet",
        "heroine",
        "heroïne",
        "meth",
        "crack",
        "مخدرات",
        "حشيش"
    ]

    return any(
        word in text_lower
        for word in drug_words
    )


def is_suicide_question(text):
    text_lower = text.lower()

    suicide_words = [
        "ik wil dood",
        "ik wil sterven",
        "ik wil niet meer leven",
        "ik wil mezelf doden",
        "ik wil mezelf pijn doen",
        "zelfmoord",
        "suicide",
        "ik zie het niet meer zitten",
        "i want to die",
        "i want to kill myself",
        "أريد أن أموت",
        "انتحار"
    ]

    return any(
        word in text_lower
        for word in suicide_words
    )


def is_recovery_question(text):
    text_lower = text.lower()

    recovery_words = [
        "ik wil afkicken",
        "ik wil stoppen met drugs",
        "ik wil stoppen met gebruiken",
        "ik wil stoppen",
        "ik ben verslaafd",
        "hulp bij verslaving",
        "afkickhulp",
        "verslavingszorg",
        "i want to stop using drugs",
        "i am addicted",
        "addiction help"
    ]

    return any(
        word in text_lower
        for word in recovery_words
    )

def get_medical_safety_response(language="Nederlands"):
    if language == "Arabisch":
        return (
            "لا أستطيع تقديم نصيحة طبية. "
            "اطلب المساعدة من أحد العاملين أو من مقدم رعاية صحية. "
            "في حالة الخطر أو الطوارئ اتصل بالرقم 112."
        )

    if language == "Engels":
        return (
            "I cannot give medical advice. "
            "Please ask a support worker or healthcare professional for help. "
            "In emergencies call 112."
        )

    return (
        "Ik kan geen medisch advies geven. "
        "Vraag hulp aan een medewerker of hulpverlener. "
        "Bij direct gevaar of spoed: bel 112."
    )


def get_drug_safety_response(language="Nederlands"):
    if language == "Arabisch":
        return (
            "لا أستطيع تقديم نصيحة حول استخدام المخدرات. "
            "اطلب المساعدة من أحد العاملين أو من مقدم رعاية."
        )

    if language == "Engels":
        return (
            "I cannot give advice about drug use. "
            "Please ask a support worker or healthcare professional for help."
        )

    return (
        "Ik kan geen advies geven over drugsgebruik. "
        "Vraag hulp aan een medewerker of hulpverlener."
    )
def get_suicide_safety_response(language="Nederlands"):
    if language == "Arabisch":
        return (
            "يبدو أنك تمر بوقت صعب جدًا. "
            "اطلب المساعدة فورًا من شخص تثق به أو من أحد العاملين. "
            "إذا كنت في خطر مباشر، اتصل بالرقم 112."
        )

    if language == "Engels":
        return (
            "It sounds like you are having a very difficult time. "
            "Please talk to a support worker, staff member, or someone you trust now. "
            "If you are in immediate danger, call 112."
        )

    return (
        "Het klinkt alsof je het heel moeilijk hebt. "
        "Praat nu met een hulpverlener, medewerker of iemand die je vertrouwt. "
        "Bij direct gevaar: bel 112. "
        "Je kunt ook contact opnemen met 113 Zelfmoordpreventie via 113 of 0800-0113."
    )


def get_recovery_response(language="Nederlands"):
    if language == "Arabisch":
        return (
            "يمكنك طلب المساعدة من Straatzorg Rotterdam أو من أحد العاملين. "
            "قل إنك تريد التوقف عن استخدام المخدرات. "
            "يمكن لمقدم الرعاية مساعدتك في الخطوة التالية."
        )

    if language == "Engels":
        return (
            "You can ask Straatzorg Rotterdam or a support worker for help. "
            "Tell them you want to stop using drugs. "
            "A professional can help you with the next step."
        )

    return (
        "Je kunt hulp vragen bij Straatzorg Rotterdam of een hulpverlener. "
        "Vertel dat je wilt stoppen met gebruiken. "
        "Een medewerker kan je helpen met de volgende stap."
    )

def get_fallback_response(language="Nederlands"):
    if language == "Arabisch":
        return (
            "لست متأكدًا بناءً على معلومات الأسئلة الشائعة المتاحة. "
            "اطلب المساعدة من Pauluskerk أو من أحد العاملين."
        )

    if language == "Engels":
        return (
            "I am not sure based on the available FAQ. "
            "Please ask the Pauluskerk or a support worker for help."
        )

    return (
        "Ik weet het niet zeker op basis van de beschikbare FAQ. "
        "Vraag hulp bij de Pauluskerk of een hulpverlener."
    )