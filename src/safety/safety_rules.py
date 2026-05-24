def detect_language(text):
    text_lower = text.lower()

    arabic_chars = any("\u0600" <= char <= "\u06FF" for char in text)

    polish_chars = any(
        char in text_lower
        for char in ["ą", "ć", "ę", "ł", "ń", "ó", "ś", "ź", "ż"]
    )

    english_words = [
        "where", "what", "how", "help", "sleep",
        "shower", "hungry", "food", "documents"
    ]

    if arabic_chars:
        return "Arabisch"

    if polish_chars:
        return "Pools"

    english_count = sum(word in text_lower for word in english_words)

    if english_count >= 2:
        return "Engels"

    return "Nederlands"


def is_medical_complaint(text):
    text_lower = text.lower()

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
        "medisch",

        "الم",
        "وجع",
        "صداع",
        "مريض",
        "دم",
        "تنفس"
    ]

    return any(word in text_lower for word in medical_words)


def is_medical_care_question(text):
    text_lower = text.lower()

    care_words = [
        "huisarts",
        "dokter",
        "arts",
        "medische hulp",
        "niet verzekerd",
        "verzekering",
        "zorg",
        "straatzorg",

        "طبيب",
        "تأمين",
        "مساعدة طبية"
    ]

    return any(word in text_lower for word in care_words)


def is_drug_question(text):
    text_lower = text.lower()

    drug_words = [
        "drugs",
        "cocaine",
        "wiet",
        "heroine",
        "verslaafd",
        "afkicken",
        "meth",
        "crack",

        "مخدرات",
        "ادمان",
        "حشيش"
    ]

    return any(word in text_lower for word in drug_words)


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
            "لا أستطيع تقديم advies over drugsgebruik. "
            "اطلب المساعدة من أحد العاملين أو من hulpverlener."
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