# Research notes (claude-2, Sat 10 Oct)

Web research behind the claude-2 ideas. Each fact has its source link. Where sources disagree, it says so. **Check again before a number goes into the deck.**

## Local context: Uzbekistan
- **Road deaths:** 2,203 deaths and 9,364 crashes in 2024 ([AKIpress](https://akipress.com/news:838901:2,203_people_die_in_traffic_accidents_in_Uzbekistan_in_2024)). 2025 figures disagree: 2,188 deaths ([Kun.uz](https://kun.uz/en/news/2026/01/14/traffic-deaths-remain-high-across-uzbekistan-despite-prevention-efforts)) vs 1,854 ([Kun.uz, 15 Jan](https://kun.uz/en/news/2026/01/15/traffic-deaths-remain-high-across-uzbekistan-despite-prevention-efforts)). Speeding = 32.9% of causes in Q1 2026, ignoring signals = 22.4% (same source).
- **Vehicle fleet:** 4.73 M vehicles owned by individuals as of 1 Oct 2025, 92.9% passenger cars ([stat.uz](https://stat.uz/en/press-center/news-of-committee/65603-zbekistonda-zhismonij-shakhslarga-tegishli-avtotransport-vositalari-soni-4-7-mlndan-oshdi-4)).
- **OSAGO (compulsory motor liability, OSGOVTS):** the insured sum doubles from 40 to 80 M soums from 1 Jan 2026 (Cabinet Resolution No. 458, 23 Jul 2025) ([podrobno.uz](https://podrobno.uz/cat/economic/limity-pokrytiya-po-osago-v-uzbekistane-uvelichat-vdvoe-s-2026-goda/), [buxgalter.uz](https://buxgalter.uz/publish/doc/text209644_kak_izmenitsya_stoimost_polisov_osago)). Bigger payouts mean more incentive for claim fraud (our inference).
- **Trade-in:** Cabinet Resolution PKM-535 (22 Aug 2025) lets manufacturers, distributors and dealers take used cars in exchange. Vehicles get technical identification against the database ([zamin.uz](https://zamin.uz/en/avto/158606-trade-in-va-trade-up-tizimi-avtohizmat-bozorida-qonuniylashdi.html), [spot.uz](https://www.spot.uz/ru/2025/08/26/trade-up/)). Dealers typically require: foreign car ≤ 7 years, no serious damage (unverified, one source).
- **EV charging:** 1,399 public stations on 1 May 2025, 820 of them in Tashkent (2.5× growth in a year) ([Daryo](https://daryo.uz/en/2025/05/04/uzbekistan-sees-2-5-fold-surge-in-ev-charging-stations-1216442/), [Kursiv](https://uz.kursiv.media/en/2025-05-04/uzbekistan-sees-number-of-ev-charging-stations-rise-2-5-times-in-one-year/)). Target: 4,000 by end of 2026 ([Kun.uz](https://kun.uz/en/news/2026/05/05/uzbekistan-to-expand-ev-charging-network-to-4000-stations-by-end-of-2026)). Every public parking lot must have at least one EV charging space (unverified, one source).
- **BYD:** local plant (Song Plus DM-i, Chazor DM-i, about 50k/yr), Ti 7 launched in Tashkent on 1–4 Oct 2026 ([CnEVPost](https://cnevpost.com/2026/10/08/byd-launches-fang-cheng-bao-tai-7-uzbekistan/), [Global Voices](https://globalvoices.org/2024/09/11/chinese-electric-car-production-kicks-off-in-uzbekistan/)).
- **Ducati:** official 3S dealership opened in Tashkent in Sept 2025, Zargar str. 4, Shayxontohur ([Ducati locator](https://www.ducati.com/be/fr/dealers/tashkent/tashkent-city-shayxontohur-distric), [blog](https://centrum-air.com/en/blogs/ducati-uzbekistan)).
- **Roads in Tashkent:** the city's complaint channel is *Xalq Nazorati* (web + app). In March 2025 the hokimiyat asked residents to send photos of poor repairs there. Critics report practically no quality control at road acceptance ([spot.uz](https://www.spot.uz/oz/2025/03/18/road-repair/), [anhor.uz](https://anhor.uz/vzglyad-iznutri/tashkent-86/), [podrobno.uz](https://podrobno.uz/cat/obchestvo/tashkentskiy-khokimiyat-zapustil-servis-dlya-zhalob-na-kommunalnoe-obsluzhivanie-plokhie-dorogi-i-dr/)). Repair plan of about 816,000 m² mentioned by the hokimiyat ([anhor.uz](https://anhor.uz/news/road-repair/)).

## Insurance photo fraud (global)
- Milliman (Dec 2025): humans spot AI-manipulated car-damage photos at about **50% accuracy**, no better than chance ([Milliman](https://www.milliman.com/en-GB/insight/accidents-that-never-happened-genai-motor-fraud)).
- Verisk: in 768,000 claim images, 1,967 duplicates were found; one photo was used in **44 different claims** ([Verisk](https://investor.verisk.com/News--Events-/Press-Releases--Market-Info/news-details/2023/Insurance-Fraud-Finds-a-New-Enemy-in-Verisks-Advanced-Image-Forensics/default.aspx)).
- A photo of a screen showing a damaged car can be indistinguishable to the eye. There are patents on recapture detection ([USPTO 11037284](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11037284)). Vendor Vaarhaft combines authenticity scan, reverse image search and secure recapture ([Vaarhaft](https://www.vaarhaft.com/resources/blog/detect-fake-insurance-claim-images)). These are vendor claims, with no independent benchmarks.
- Inspection vendors (Tchek, ProovStation, Monk, DeGould) publish no prices. The only public per-unit price found is VerifyAI at $0.008 per photo verification, on a competitor-written page ([switchlabs](https://www.switchlabs.dev/compare/verify-ai-vs-tchek)).

## Models: licences matter for the business slide
| Model | Licence | Note |
|---|---|---|
| Ultralytics YOLOv8 / YOLO11 | AGPL-3.0 (commercial = paid Enterprise) | fine for a public hackathon repo; a cost line in the business plan |
| RF-DETR (Nano → Large) | Apache-2.0 ([Roboflow](https://blog.roboflow.com/rf-detr/)) | "Plus" checkpoints have their own licence; better for few labels (DINOv2 backbone), vendor claim |
| Florence-2 | MIT ([Roboflow](https://playground.roboflow.com/models/compare/florence-2-vs-owl-vit)) | open-vocabulary detection by text prompt |
| OWL-ViT / OWLv2 | Apache-2.0 for OWL-ViT; check the OWLv2 card | zero-shot text-query detector |
| Depth Anything V2 (Small) | check the card | dashcam depth reasonable only up to about 15 m, flickers between frames ([arXiv 2508.11591](https://arxiv.org/pdf/2508.11591)) |

## Datasets
| Dataset | Licence (verify) | Use |
|---|---|---|
| RDD2022, 47,420 road images, 6 countries ([figshare](https://figshare.com/articles/dataset/RDD2022_-_The_multi-national_Road_Damage_Dataset_released_through_CRDDC_2022/21431547), [paper](https://arxiv.org/abs/2209.08538v1)) | **conflict:** CC BY-SA 4.0 ([Dataset Ninja](https://datasetninja.com/road-damage-detector)) vs CC BY 4.0 (OSM forum). Read the figshare record | road damage |
| Road-damage YOLOv8n/v10n/11n weights ([HF nsr51324](https://huggingface.co/nsr51324/Road_Damage_Object_Detection)) | no licence on the card. Inherits AGPL from Ultralytics? Ask or avoid | quick start |
| CarDD, 4,000 images, 6 damage classes ([site](https://cardd-ustc.github.io), [paper](https://arxiv.org/pdf/2211.00945)) | **non-commercial research only**; images under Flickr/Shutterstock terms | benchmark only, not product |
| Roboflow car damage, CC BY 4.0: [damaged-cars-5cs3k](https://universe.roboflow.com/scratchscn/damaged-cars-5cs3k) (369 images, YOLO11-seg), [damage_detection-az44j](https://universe.roboflow.com/transporter/damage_detection-az44j) (1,310 images), [car-damage-4-classes](https://universe.roboflow.com/dhananjay-sangle-waupz/car-damage-4-classes) | CC BY 4.0 (attribution) | car damage training |
| Central Asia plates ([Mendeley 10.17632/4c5z833m6m.2](https://data.mendeley.com/datasets/4c5z833m6m/2)) | check | Uzbek plate format: 3 letters + 5 digits per the description |
| Helmet: EdgeVision, 2,392 images ([Mendeley](https://data.mendeley.com/datasets/j82bnw7gsr)) | check | rider helmet |
| Mapillary street-level images ([licence](https://help.mapillary.com/hc/en-us/articles/115001770409-Licenses)) | CC BY-SA, plus Mapillary terms for commercial use | **local Tashkent road images** for a test set; check whether the API serves blurred faces and plates |

## Deployment
- Hugging Face Spaces: CPU Basic = 2 vCPU / 16 GB, free per the docs. **But** 2026 forum reports say free accounts get a "cpu-basic quota" 403 on Docker/Gradio Spaces and need PRO or credits ([HF docs](https://huggingface.co/docs/hub/en/spaces-overview), [forum](https://discuss.huggingface.co/t/403-cpu-basic-quota-limit-on-my-first-and-only-space/178658)). Free Spaces also sleep when idle. **Test early** and keep a fallback (Render / Railway / own VPS + GitHub Actions).

## What judges reward (synthesis)
- The rubric for this event (from [hackathon.wiut.uz](https://hackathon.wiut.uz/tracks/computer-vision/)): innovation, tech and impact at 25% each. "Just wrapping an API" is scored low ([reskilll](https://blogs.reskilll.com/what-hackathon-judges-look-for-complete-judging-criteria-breakdown-2026/)).
- Best defences against the replication test: **our own data** (local photos we collect, e.g. screen recaptures, Tashkent roads), a multi-stage pipeline with measured failure modes, and process integration (who acts on the output).
