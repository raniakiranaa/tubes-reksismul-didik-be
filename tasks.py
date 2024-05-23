import random

correct_words = [
    "buku", "makan", "jalan", "bunga", "pulau", "pakai", "rumah", "sekolah",
    "belajar", "lipat", "membaca", "bermain", "tidur", "minum", "berlari",
    "kerja", "teman", "indah", "melihat", "pergi", "kembali", "tulis", "dengar",
    "main", "lari", "duduk", "bangun", "baca", "jaga", "pikir", "nyanyi",
    "masak", "pulang", "renang", "mendengar", "suka", "belanja", "tonton",
    "senang", "pikir", "tanya", "jawab", "bicara"
]

incorrect_words = [
    "yegak", "hayuk", "semungut", "yekali", "masasi", "yaelah", "sumpah",
    "cuan", "galau", "lebay", "kepoo", "mager", "gabut", "baper", "labil",
    "ciye", "hallo", "asik", "seru", "cihui", "gokil", "wkwk", "jomblo",
    "nyok", "tobat", "greget", "kuy", "hoax", "ilfeel", "pelakor", "baper",
    "lebay", "alay", "rempong", "sok", "cihuy", "galau", "gaje", "julid",
    "modus", "nolep", "prikitiw", "santuy", "tajir", "zonk", "halu"
]

def generate_tasks(num_tasks=10, words_per_task=18):
    tasks = []
    for _ in range(num_tasks):
        selected_correct_words = random.sample(correct_words, words_per_task // 2)
        selected_incorrect_words = random.sample(incorrect_words, words_per_task // 2)
        selected_words = selected_correct_words + selected_incorrect_words
        random.shuffle(selected_words)
        tasks.append({
            "words": selected_words,
            "correct": selected_correct_words
        })
    return tasks

tasks = generate_tasks()
