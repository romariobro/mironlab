"""Build the bilingual MironLab media archive from the portfolio registry."""
import html
import json
import shutil
from pathlib import Path

SOURCE = Path(r"C:\Users\CarbonX\OneDrive\Документы\GitHub\projectportfolio")
OUT = Path(__file__).parent / "media"
registry = json.loads((SOURCE / "data/media.json").read_text(encoding="utf-8"))
ORDER = ["A01","P08","B01","B02","B03","B04","S01","D05","D01","D04","D03","E04","C01","C02","C03","C04","F01","F02","F03","F05","F06","F07","A02","A03","A04","P09"]
records = sorted((r for r in registry["records"] if r["published"] and r["id"] in ORDER), key=lambda r: ORDER.index(r["id"]))
TRANSLATIONS = {
 "E01": ("Расчётные решения, «Стрелка» и транспортный процессинг", "Компания и отраслевая инфраструктура обработки транспортных платежей."),
 "E02": ("Банковская карта как единый проездной", "Независимая публикация о безналичной оплате проезда."),
 "E04": ("АО «Расчётные решения» — официальный сайт", "Официальный источник о компании и её продуктах платёжной инфраструктуры."),
 "D01": ("Как покупка квартиры стала полностью онлайн", "Публикация компании о дистанционной покупке квартиры и изменениях во время COVID-19."),
 "D03": ("Росбанк и Самолёт проводят ипотечные сделки онлайн", "Независимая публикация об онлайн-ипотеке."),
 "D04": ("Как купить квартиру не выходя из дома", "Публикация о полном дистанционном пути покупки квартиры."),
 "D05": ("Купить квартиру за чашкой кофе", "Партнёрский материал об упрощении цифрового пути покупки жилья."),
 "P08": ("Во сколько работодателям обходится игнорирование эмоциональной подавленности работников", "Статья с комментарием Романа Мироничева об эмоциональном состоянии сотрудников, продуктивности и влиянии на бизнес."),
 "B01": ("SIMDAQ привлёк $5 млн в рамках Waves Lab", "Независимая публикация об инвестициях в SIMDAQ и программе инкубации Waves Lab."),
 "B02": ("SIMDAQ вошёл в инкубатор Waves Lab", "Независимая публикация о первых проектах Waves Lab."),
 "B03": ("SIMDAQ: маркетплейс торговых стратегий", "Обзор симулятора торговли на исторических данных и концепции маркетплейса стратегий."),
 "B04": ("Маркетплейс SIMDAQ на смарт-контрактах Waves", "Официальная публикация проекта о механике маркетплейса и первом релизе."),
 "S01": ("Презентация платформы SIMDAQ", "Публичное видео с демонстрацией платформы. Не является подтверждением личного выступления Романа."),
 "C01": ("Gamblica: цифровой игровой продукт", "Независимая публикация о концепции и запуске международного цифрового продукта."),
 "C02": ("Gamblica: онлайн-платформа", "Спонсорский материал о продукте, а не независимая редакционная рекомендация."),
 "C03": ("Gamblica: публикация о кампании финансирования", "Пресс-релиз о продукте и кампании привлечения финансирования."),
 "C04": ("Gamblica: профиль проекта", "Профиль в каталоге, сохранённый как ссылка на продукт."),
 "F01": ("Интервью Aether Games: продуктовая концепция и AR", "Независимое интервью о продукте портфеля и его позиционировании."),
 "F02": ("Cards of Ethernity в каталоге Razer", "Сторонний каталог продукта как свидетельство международного выпуска."),
 "F03": ("Как Red Rift изменил рынок интерактивных историй", "Официальная публикация компании о продукте StorySpark."),
 "F05": ("Berserk: The Cataclysm — видео продукта", "Публичное видео продукта. Исходный домен проекта недоступен."),
 "F06": ("Puzzle Royale — документация продукта", "Публичная документация продукта."),
 "F07": ("Cards of Ethernity — видео продукта", "Публичное видео. Исходный домен coe.gg теперь относится к другому продукту и не используется."),
 "A01": ("Интерактивная реклама: как продвигаются BBC, Mercedes-Benz и Discovery", "Авторская публикация об интерактивной рекламе и примерах международных брендов."),
 "A02": ("Как я управлял проектами в IT и GameDev, и что из этого понял — Часть 1", "Практическая статья о командах, неопределённости, MVP и delivery в IT и игровой разработке."),
 "A03": ("Часть 2. Почему система управления в проекте — это не просто «доска задач». От проблем к решениям", "Практическая статья о системе управления проектом и переходе от разрозненных задач к управляемому исполнению."),
 "A04": ("Про зарплаты проджектов ИТ, человеческое отношение к сотрудникам и ИИ в проектном менеджменте — Часть 3", "Авторская статья об оплате труда, отношении к команде и применении ИИ в проектной работе."),
 "P09": ("ПОговорим за виртуалку?", "Обзор с комментарием Романа Мироничева об инструментах совместной работы, удалёнке и коммуникациях.")
}
EN_TITLES = {
 "A01": "Interactive advertising: how BBC, Mercedes-Benz and Discovery promote their brands",
 "A02": "What I learned managing IT and game development projects — Part 1",
 "A03": "Why a project management system is more than a task board — Part 2",
 "A04": "IT project manager pay, humane leadership and AI in project management — Part 3",
 "P08": "The cost of ignoring employees’ emotional distress",
 "P09": "Let’s talk about virtual collaboration"
}
GROUPS = {
 "By Me": "Мои статьи", "Speaking": "Выступления", "Projects in the Media": "Проекты в СМИ",
 "Personal Mentions": "Комментарии и упоминания", "References": "Ссылки на продукты"
}
TOPICS = {"AI":"ИИ","Project Management":"Управление проектами","Product":"Продукт","FinTech":"Финтех","GameDev":"Игровая разработка","Blockchain":"Блокчейн","Real Estate":"Недвижимость","Digital Transformation":"Цифровая трансформация","Marketing":"Маркетинг","PR":"PR","Growth":"Рост","Management":"Управление","Operations":"Операции","Product Operations":"Product Operations"}
def e(value): return html.escape(str(value), quote=True)
def tr(ru, en, lang): return ru if lang == "ru" else en
def section(r, lang):
    i = r["id"]
    if i == "A01": return "ThingLink"
    if i.startswith("E"): return tr("Расчётные решения","Raschetnye Resheniya",lang)
    if i.startswith("D"): return tr("Самолёт","Samolet",lang)
    if i == "P08": return tr("Эмоциональный интеллект","Emotional Intelligence",lang)
    if i.startswith("B") or i == "S01": return "SIMDAQ"
    if i.startswith("C"): return tr("Международные стартапы","International Startups",lang)
    if i.startswith("F"): return tr("Игры и цифровые продукты","Games & Digital Products",lang)
    return tr("Статьи и другие публикации","Articles & Other Media",lang)
def title(r, lang): return TRANSLATIONS[r["id"]][0] if lang == "ru" else EN_TITLES.get(r["id"],r["title"])
def about(r, lang):
    clean = {
      "F02": ("Карточная игра Cards of Ethernity в каталоге Razer.","Cards of Ethernity, a card game listed on Razer."),
      "F05": ("Видеопрезентация Berserk: The Cataclysm.","Berserk: The Cataclysm product video."),
      "F06": ("Документация Puzzle Royale: концепция игры и развитие продукта.","Puzzle Royale documentation: game concept and product development."),
      "F07": ("Видеопрезентация Cards of Ethernity.","Cards of Ethernity product video."),
      "S01": ("Демонстрация торгового симулятора SIMDAQ.","A demonstration of the SIMDAQ trading simulator."),
      "C02": ("Спонсорская публикация о платформе Gamblica.","Sponsored coverage of the Gamblica platform."),
      "C04": ("Профиль Gamblica: концепция и описание продукта.","Gamblica profile: product concept and overview.")
    }
    if r["id"] in clean: return clean[r["id"]][0 if lang=="ru" else 1]
    return TRANSLATIONS[r["id"]][1] if lang == "ru" else r["about"]
def role(r, lang):
    if lang == "en":
        i=r["id"]
        if i.startswith("F"): return "Head of PMO / Product Delivery at REDRIFT."
        if i.startswith("B") or i=="S01": return "Product Management / Growth Operations: MVP, roadmap, gamification and international launch."
        if i.startswith("C"): return "Product / PMO / Operations: roadmap, MVP, launch and cross-functional coordination."
        if i.startswith("D"): return "Digital transformation of marketing and commercial operations; transformation portfolio PMO."
        return r["role"]
    i=r["id"]
    if i.startswith("E"): return "Руководство транспортным платёжным процессингом: приоритизация, roadmap, разработка, релизы и масштабирование."
    if i.startswith("D"): return "Цифровая трансформация маркетинга и коммерции; управление проектным офисом портфеля."
    if i == "P08": return "Экспертный комментарий / генеральный директор Exiclub."
    if i == "P09": return "Экспертный комментарий / основатель Privetmarketing."
    if i == "A01": return "Автор / директор по развитию бизнеса ThingLink Russia."
    if i.startswith("A"): return "Автор — Роман Мироничев / RomarioHabr."
    if i.startswith("B") or i=="S01": return "Product Management / Growth Operations: MVP, roadmap, геймификация и международный запуск."
    if i.startswith("C"): return "Product / PMO / Operations: roadmap, MVP, запуск и координация функций."
    return "Head of PMO / Product Delivery в REDRIFT."
def date(r, lang):
    return r["date"] if r["date"] else tr("Дата публикации не указана","Publication date not provided",lang)
def langlabel(r, lang):
    return tr("Оригинал на русском","Original in Russian",lang) if r["language"]=="ru" else tr("Оригинал на английском","Original in English",lang)
def navigation(lang, root, alternate):
    home=root+"../"
    return f'<header class="media-nav"><a class="brand" href="{home}">MIRONLAB</a><nav><a href="{home}projects.html">{tr("Проекты","Projects",lang)}</a><a href="{root if lang=="ru" else root+"en/"}">{tr("Медиа","Media",lang)}</a><a href="{home}#contact">{tr("Контакты","Contact",lang)}</a><a class="language-link" href="{alternate}" lang="{tr("en","ru",lang)}">{tr("EN","RU",lang)}</a></nav></header>'
def page(lang, content, root, alternate, page_title):
    return f'<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><title>{e(page_title)} — MironLab</title><meta name="description" content="{e(tr("Статьи, интервью и публикации о проектах Романа Мироничева.","Articles, interviews and coverage of Roman Mironichev’s projects.",lang))}"><link rel="stylesheet" href="{root}../jump.css?v=dark-restored"><link rel="stylesheet" href="{root}media.css?v=1"></head><body>{navigation(lang,root,alternate)}<main class="media-shell">{content}</main><footer><a href="{root}../">MironLab — Roman Mironichev</a><a href="{root if lang=="ru" else root+"en/"}">{tr("Все публикации","All publications",lang)}</a></footer><script src="{root}media.js?v=1" defer></script></body></html>'
def card(r, lang, root):
    label=GROUPS.get(r["group"],r["group"]) if lang=="ru" else r["group"]
    tags=" · ".join(TOPICS.get(t,t) if lang=="ru" else t for t in r["topics"])
    return f'<article class="media-card" data-group="{e(r["group"])}" data-topics="{e("|".join(r["topics"]))}"><a href="{e(r["slug"])}/"><img src="{root}images/{e(Path(r["image"]).name)}" alt="{e(title(r,lang))}" loading="lazy" width="800" height="450"></a><div class="card-copy"><div class="source">{e(r["source"])}</div><div class="meta">№ {r["publication_number"]} · {date(r,lang)}<br>{langlabel(r,lang)} · {e(label)}</div><h3><a href="{e(r["slug"])}/">{e(title(r,lang))}</a></h3><p>{e(about(r,lang))}</p><p class="tags">{e(tags)}</p><div class="actions"><a href="{e(r["slug"])}/">{tr("Подробнее","Details",lang)} →</a><a href="{e(r["url"])}" target="_blank" rel="noopener noreferrer">{tr("Оригинал","Original",lang)} ↗</a></div></div></article>'
def build():
    OUT.mkdir(exist_ok=True)
    (OUT/"images").mkdir(exist_ok=True)
    for r in records:
        assert r["id"] in TRANSLATIONS, r["id"]
        shutil.copy2(SOURCE/r["image"], OUT/"images"/Path(r["image"]).name)
    for lang in ("ru","en"):
        base=OUT if lang=="ru" else OUT/"en"
        base.mkdir(exist_ok=True)
        root="./" if lang=="ru" else "../"
        alternate="en/" if lang=="ru" else "../"
        intro=tr("Избранные статьи, интервью и публикации о моей работе в разработке продуктов, управлении проектами, технологиях, маркетинге и цифровой трансформации.","Selected articles, interviews and media coverage related to my work in product development, project management, technology, marketing and digital transformation.",lang)
        attribution=tr("Здесь собраны мои публикации и материалы о продуктах и компаниях, над которыми я работал. Моя роль указана отдельно на странице каждого материала.","The collection includes my own publications and coverage of products and companies I worked with. My role is listed separately on each material’s page.",lang)
        heading=tr("Медиа и публикации","Media & Publications",lang)
        content=f'<section class="media-intro"><h1>{heading}</h1><p>{intro}</p><p>{attribution}</p><a href="#all-media">{tr("Материалов: ","Materials: ",lang)}{len(records)} ↓</a></section>'
        filters=''.join(f'<button type="button" data-filter-group="{e(g)}" aria-pressed="false">{e(GROUPS[g] if lang=="ru" else g)}</button>' for g in GROUPS if any(r["group"]==g for r in records))
        topics=sorted({t for r in records for t in r["topics"]})
        content+=f'<section id="all-media"><h2>{tr("Все публикации","All Media",lang)}</h2><div class="filters"><button type="button" data-filter-group="All" aria-pressed="true">{tr("Все","All",lang)}</button>{filters}</div><label class="topic-label">{tr("Тема","Topic",lang)} <select id="topic"><option value="All">{tr("Все темы","All topics",lang)}</option>{"".join(f"<option value=\"{e(t)}\">{e(TOPICS.get(t,t) if lang=="ru" else t)}</option>" for t in topics)}</select></label><p id="results-count" aria-live="polite"></p>'
        groups={}
        for r in records: groups.setdefault(section(r,lang),[]).append(r)
        for name,items in groups.items():
            content+=f'<section class="media-group"><h2>{e(name)}</h2><div class="media-grid all-grid">{"".join(card(r,lang,root) for r in items)}</div></section>'
        content+=f'<p id="empty" hidden>{tr("Нет материалов с такими фильтрами.","No materials match these filters.",lang)}</p></section>'
        (base/"index.html").write_text(page(lang,content,root,alternate,heading),encoding="utf-8")
        for r in records:
            folder=base/r["slug"]; folder.mkdir(exist_ok=True)
            detail_root="../" if lang=="ru" else "../../"
            alternate=f'../en/{r["slug"]}/' if lang=="ru" else f'../../{r["slug"]}/'
            credit=tr("Изображение из оригинального источника","Image from the original source",lang) if r["image_origin"]=="original" else tr("Изображение из портфолио проекта","Image from the project portfolio",lang)
            content=f'<article class="detail"><a href="../">← {tr("Все публикации","All Media",lang)}</a><p class="source">{e(r["source"])}</p><p class="meta">№ {r["publication_number"]} · {date(r,lang)} · {langlabel(r,lang)}</p><h1>{e(title(r,lang))}</h1><img class="detail-image" src="{detail_root}images/{e(Path(r["image"]).name)}" alt="{e(title(r,lang))}"><p class="meta">{credit}</p><p>{e(about(r,lang))}</p><h2>{tr("Моя роль","My role",lang)}</h2><p>{e(role(r,lang))}</p><a class="button" href="{e(r["url"])}" target="_blank" rel="noopener noreferrer">{tr("Открыть оригинал","Open original",lang)} ↗</a></article>'
            (folder/"index.html").write_text(page(lang,content,detail_root,alternate,title(r,lang)),encoding="utf-8")
    (OUT/"source-registry.json").write_text(json.dumps(registry,ensure_ascii=False,indent=2),encoding="utf-8")
    print(f"Built {len(records)} materials in RU and EN; {len(records)*2+2} HTML pages.")
if __name__=="__main__": build()
