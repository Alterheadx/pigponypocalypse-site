# одноразово: превращает английские страницы в шаблоны {{key}} и пишет i18n/en.json
import json, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
B = os.path.join(ROOT, "_build")

COMMON = [
    ("boss1", "Arcane Corrupted Piglet"),
    ("boss2", "Swying Swyan"),
    ("boss3", "Boar Sentinel"),
    ("boss4", "The Swine King"),
    ("wishlist", "Wishlist on Steam"),
    ("watch_yt", "Watch on YouTube"),
    ("tag_a", "Four bosses. No filler."),
    ("tag_b", "Every death is on you."),
]

LANDING = [
    ("l_title", "<title>PigPonyPocalypse — Hardcore Boss Rush</title>"),
    ("l_meta", "PigPonyPocalypse: four bosses that punish every mistake, two difficulties and a global DPS leaderboard. Out October 13, 2026 on Steam for Windows and macOS."),
    ("og_desc", "Four bosses. No filler. Every death is on you. Out October 13, 2026 on Steam."),
    ("l_hero_alt", "Three pony heroes on a lava ledge facing the Swine King and his bosses"),
    ("l_menu_trailer", ">Watch the trailer<"),
    ("l_menu_bosses", ">The bosses<"),
    ("presskit", ">Press kit<"),
    ("l_date", "Out <b>13.10.2026</b> · Steam · Windows &amp; macOS"),
    ("l_st_bosses", "<span>Bosses</span>"),
    ("l_st_diff", "<span>Difficulties</span>"),
    ("l_st_talents", "<span>Talents</span>"),
    ("l_st_lb", "<span>DPS leaderboards</span>"),
    ("l_st_grind", "<span>Grind</span>"),
    ("l_trailer_h", "<h2>Trailer</h2>"),
    ("l_bosses_h", "Learn the patterns. Die. Try again."),
    ("l_bosses_lead", "Every boss plays by its own rules. True Challenge adds new phases and mechanics to every fight, and your best DPS goes to a global Steam leaderboard."),
    ("l_b1n", '<span class="n">Boss 1</span>'),
    ("l_b2n", '<span class="n">Boss 2</span>'),
    ("l_b3n", '<span class="n">Boss 3</span>'),
    ("l_b4n", '<span class="n">Boss 4 · Final</span>'),
    ("l_b1d", "Corrupted ground, towers, boars, and the lights go out."),
    ("l_b2d", "Outrun the wall of fire, then fight two brothers at once."),
    ("l_b3d", "Where you stand decides how the Sentinel fights."),
    ("l_b4d", "Four phases, and every purified boss fights at your side."),
    ("l_motion", "<h2>In motion</h2>"),
    ("clip1", "Four spears, one cross"),
    ("clip2", "Lights out"),
    ("clip3", "Outrun the fire"),
    ("clip4", "Get under the dome"),
    ("l_final", "<h2>Out October 13 on Steam</h2>"),
]

PRESS = [
    ("p_title", "<title>PigPonyPocalypse — Press Kit</title>"),
    ("p_meta", "Press kit for PigPonyPocalypse, a hardcore boss rush out October 13, 2026 on Steam. Fact sheet, bosses, screenshots, clips, logo and press contact."),
    ("og_desc", "Four bosses. No filler. Every death is on you. Out October 13, 2026 on Steam."),
    ("p_og_title", '"PigPonyPocalypse — Press Kit"'),
    ("p_hero_alt", "Key art: three pony heroes on a lava ledge facing the Swine King, the Arcane Corrupted Piglet, the Boar Sentinel and the twin boars Swying Swyan"),
    ("p_out", "<b>Out October 13, 2026</b>"),
    ("p_steam_page", ">Steam page<"),
    ("p_shots_clips", ">Screenshots &amp; clips<"),
    ("p_dl_zip", ">Download ZIP<"),
    ("p_press_contact_btn", '<a class="btn" href="#contact">Press contact</a>'),
    ("p_facts", ">Fact sheet<"),
    ("p_f_title", "<dt>Title</dt>"),
    ("p_f_dev", "<dt>Developer</dt>"),
    ("p_f_dev_v", "Alterhead (solo developer, self-published)"),
    ("p_f_rel", "<dt>Release</dt>"),
    ("p_f_rel_v", "<dd>October 13, 2026</dd>"),
    ("p_f_plat", "<dt>Platforms</dt>"),
    ("p_f_plat_v", "Windows, macOS (Steam)"),
    ("p_f_genre", "<dt>Genre</dt>"),
    ("p_f_genre_v", "Boss rush, bullet hell, twin-stick shooter"),
    ("p_f_content", "<dt>Content</dt>"),
    ("p_f_content_v", "4 bosses × 2 difficulties, 9 talents, 18 Steam achievements, 8 global DPS leaderboards"),
    ("p_f_lang", "<dt>Languages</dt>"),
    ("p_f_lang_v", "English, Russian, Simplified Chinese, Japanese, Korean"),
    ("p_f_ctrl", "<dt>Controls</dt>"),
    ("p_f_ctrl_v", "Keyboard &amp; mouse; Xbox and PlayStation controllers supported"),
    ("p_f_music", "<dt>Music</dt>"),
    ("p_f_music_v", "Original metal soundtrack"),
    ("p_f_press", "<dt>Press</dt>"),
    ("p_about_eb", ">About the game<"),
    ("p_about_h", "A boss rush that punishes every mistake"),
    ("p_lede", "PigPonyPocalypse is four hand-built boss fights and nothing else. No levels, no grind, no trash enemies. Just you, the boss's patterns, and a global DPS leaderboard."),
    ("p_par1", "Every boss plays by its own rules. Some attacks can only be survived behind cover. Casts have to be interrupted. Curses stack while you get greedy with damage. Floor tiles explode in an order you'll need to memorize, then explode again with no warning at all."),
    ("p_par2", "<strong>Forgiving</strong> difficulty is there to learn the fight. <strong>True Challenge</strong> is the real game: new phases, new deadly mechanics and a different rhythm for every boss."),
    ("p_par3", "Beating a boss is half the job. Your best DPS on each boss and difficulty goes to a global Steam leaderboard, so the fight keeps going after the kill: pick from nine talents, find a better opener, squeeze out more damage than everyone else."),
    ("p_par4", "You don't fight alone, but your party won't make it easier. Facewall the tank dreams of getting punched in the face and rates every boss on its hits. Shawty the healer flat-out refuses to heal him. Command both, and freeze time when everything falls apart at once."),
    ("p_ft1h", "<h3>Every death is on you</h3>"),
    ("p_ft1p", "Every attack is telegraphed and every mechanic can be solved. No random one-shots, no stat checks you can grind past."),
    ("p_ft2h", "<h3>True Challenge</h3>"),
    ("p_ft2p", "The hard mode is a different fight: extra phases, new mechanics and tighter timings on every boss."),
    ("p_ft3h", "<h3>Out-DPS the world</h3>"),
    ("p_ft3p", "Eight Steam leaderboards rank damage per second, one per boss and difficulty. Your talents show up next to your score."),
    ("p_ft4h", "<h3>Nine talents</h3>"),
    ("p_ft4p", "Three tiers of talents change how you deal damage, from burst windows to a time loop."),
    ("p_ft5h", "<h3>A party with opinions</h3>"),
    ("p_ft5p", "Command a masochist tank and a healer who won't heal him. Freeze time to line up your moves when the screen fills up."),
    ("p_ft6h", "<h3>Metal soundtrack</h3>"),
    ("p_ft6p", "Original metal written for every fight, plus comic-book cutscenes before each boss."),
    ("p_bosses_eb", ">The bosses, in order<"),
    ("p_bosses_h", "Four fights, each with its own rules"),
    ("p_b1_alt1", "Arcane Corrupted Piglet fires spirals of arcane orbs at the player"),
    ("p_b1_alt2", "The arena goes dark while Chasing Boars hunt the player"),
    ("p_b1_alt3", "Victory screen with the DPS breakdown by ability"),
    ("p_b1_ord", ">Boss 1 of 4<"),
    ("p_b1_txt", "Looks harmless. Corrupts the ground under your hooves, summons towers and boars, and on True Challenge adds a third phase built around Arcane Annihilation."),
    ("p_b1_m1", "<b>Darkness</b> — the lights go out while Chasing Boars hunt you down."),
    ("p_b1_m2", "<b>Detonation</b> — someone has to stand in the circle, or everyone takes the blast."),
    ("p_b1_m3", "<b>Annihilation</b> — the whole arena burns; only the towers give cover."),
    ("p_b2_alt1", "Swying and Swyan fight together in the temple arena"),
    ("p_b2_alt2", "Running across the crystal bridge ahead of the wall of fire"),
    ("p_b2_ord", ">Boss 2 of 4<"),
    ("p_b2_txt", "Twin boars, one of the sun and one of the moon. Outrun a wall of fire across a crumbling bridge, then face the brothers in their arena. Kill one and the other flies into a rage."),
    ("p_b2_m1", "<b>Wall of Fire</b> — the bridge breaks behind you and the fire never stops."),
    ("p_b2_m2", "<b>Flying Boars</b> — homing orbs from above while you pick your tiles."),
    ("p_b2_m3", "<b>Orb Maze</b> — Swying fills the arena with a moving maze of orbs."),
    ("p_b3_alt1", "Boar Sentinel fires lasers across the temple floor"),
    ("p_b3_alt2", "A storm of lightning strikes covers the Sentinel's arena"),
    ("p_b3_ord", ">Boss 3 of 4<"),
    ("p_b3_txt", "The arena is split in three, and the Sentinel fights differently in each part. Where you stand decides what kills you."),
    ("p_b3_m1", "<b>Left side</b> — Lightning Strike; Pony Power recharges faster."),
    ("p_b3_m2", "<b>Right side</b> — Arcane Line sweeps the floor; your damage keeps growing."),
    ("p_b3_m3", "<b>Center</b> — the Sentinel vanishes and leaves you a Memory Puzzle."),
    ("p_b3_enr", "Enrage: <b>4 minutes</b>"),
    ("p_b4_alt1", "The Swine King channels the Royal Pyre while fire floods the hall"),
    ("p_b4_alt2", "Fire Cross lines cut through the King's hall"),
    ("p_b4_alt3", "Walls of fire split the arena into tiles"),
    ("p_b4_alt4", "The Boar General's sword slam lines radiate across the hall"),
    ("p_b4_ord", ">Boss 4 of 4 · Final<"),
    ("p_b4_txt", "Four phases, one for every quarter of his health. The bosses you defeated and purified come back to fight at your side, and in the last phase the King throws everything at you at once."),
    ("p_b4_m1", "<b>Fire Cross</b> — plant the spears so the cross burns through all of them."),
    ("p_b4_m2", "<b>Boar General</b> — a shielded second boss with his own volleys and kamikaze piglets."),
    ("p_b4_m3", "<b>Fire Memory</b> — five tiles of six explode; then the same order again, blind."),
    ("p_b4_m4", "<b>Royal Pyre</b> — break the spears' shields and interrupt the King, or the hall burns."),
    ("p_b4_enr", "Enrage: <b>7.5 minutes</b>"),
    ("p_media_eb", '<p class="eyebrow">Media</p>'),
    ("p_media_h", "Trailer, clips, screenshots"),
    ("p_dl_trailer", "Download trailer (MP4, 1080p, 41 MB)"),
    ("p_embed", "1:23 · embed it from YouTube:"),
    ("p_clips_h", "<h3>Short clips</h3>"),
    ("p_clip1_aria", "Four spears, one cross: the Swine King's Fire Cross"),
    ("p_clip2_aria", "When the lights go out, the boars come"),
    ("p_clip3_aria", "Outrun the wall of fire on the twins' bridge"),
    ("p_clip4_aria", "Get under the dome before King's Fury"),
    ("p_shots_h", "<h3>Screenshots</h3>"),
    ("p_shots_n", "11 shots · click to enlarge"),
    ("p_dl_pk", "Download press kit (ZIP, 13 MB)"),
    ("p_dl_pk_note", "11 screenshots in 4K, logo with transparency, key art. All screenshots are real gameplay."),
    ("p_art_h", "<h3>Logo &amp; key art</h3>"),
    ("p_cap_alt", "Main capsule art with the PigPonyPocalypse logo"),
    ("p_cap_cap", "<figcaption>Key art with logo</figcaption>"),
    ("p_logo_alt", '"PigPonyPocalypse logo"'),
    ("p_logo_cap", "<figcaption>Logo, transparent PNG</figcaption>"),
    ("p_dev_eb", ">Developer<"),
    ("p_dev_h", "Made by Alterhead"),
    ("p_dev_p1", "Alterhead is a solo developer: PigPonyPocalypse was designed and built by one person. The goal was a boss rush for players who want a real, fair challenge, where getting better is the only way forward and the leaderboard shows exactly how good you got."),
    ("p_dev_p2", "Steam keys for press and content creators are sent directly by email. Need a key, or more keys for your team or a giveaway? Write to the press address on this page."),
    ("p_contact_eb", '<p class="eyebrow">Press contact</p>'),
    ("p_copy", ">Copy</button>"),
    ("p_footer", "Screenshots and art may be used for coverage of the game."),
    ("p_viewer", '"Image viewer"'),
    ("p_prev", '"Previous image"'),
    ("p_next", '"Next image"'),
    ("p_close", ">Close</button>"),
    ("g1", "Arcane Corrupted Piglet — arcane spirals"),
    ("g2", "Arcane Corrupted Piglet — Darkness and Chasing Boars"),
    ("g3", "Swying Swyan — the twins' arena"),
    ("g4", "Swying Swyan — the bridge and the Wall of Fire"),
    ("g5", "Boar Sentinel — lasers"),
    ("g6", "Boar Sentinel — Lightning Strike"),
    ("g7", "The Swine King — Fire Cross"),
    ("g8", "The Swine King — walls of fire"),
    ("g9", "The Swine King — the Boar General"),
    ("g10", "The Swine King — Royal Pyre"),
    ("g11", "Victory screen — DPS breakdown"),
    ("p_enlarge", '"Enlarge: "'),
    ("p_copied", '"Copied"'),
    ("p_selected", '"Selected"'),
]

OPTIONAL = {k for k, _ in COMMON}

# в шаблон кладём только текст: обрамляющую разметку оставляем
WRAP = re.compile(r'^(<[^>]+>|>|")(.*?)(</[^>]+>|<|"|</button>)$', re.S)

def split(en):
    m = WRAP.match(en)
    if m and m.group(2) and "<" not in m.group(2):
        return m.group(1), m.group(2), m.group(3)
    return "", en, ""

def templatize(path, pairs, strings):
    s = open(path, encoding="utf-8").read()
    for key, en in sorted(pairs, key=lambda p: -len(p[1])):
        pre, text, post = split(en)
        if en not in s:
            if key in OPTIONAL: continue
            raise SystemExit(f"не найдено в {os.path.relpath(path, ROOT)}: {key} = {en!r}")
        s = s.replace(en, pre + "{{" + key + "}}" + post)
        strings[key] = text
    return s

strings = {}
landing = templatize(os.path.join(ROOT, "index.html"), COMMON + LANDING, strings)
press = templatize(os.path.join(ROOT, "presskit", "index.html"), COMMON + PRESS, strings)

# пути пресс-кита — абсолютные (страница будет и в /ja/presskit/)
for a, b in [('src="img/', 'src="/presskit/img/'), ('src="shots/', 'src="/presskit/shots/'),
             ('src="clips/', 'src="/presskit/clips/'), ('poster="clips/', 'poster="/presskit/clips/'),
             ('href="PigPonyPocalypse_PressKit.zip"', 'href="/presskit/PigPonyPocalypse_PressKit.zip"'),
             ('i.src="shots/"', 'i.src="/presskit/shots/"')]:
    press = press.replace(a, b)
press = press.replace('<a href="/">pigponypocalypse.com</a>', '<a href="{{base}}/">pigponypocalypse.com</a>')
landing = landing.replace('href="/presskit/"', 'href="{{base}}/presskit/"')

os.makedirs(os.path.join(B, "i18n"), exist_ok=True)
open(os.path.join(B, "landing.html"), "w", encoding="utf-8").write(landing)
open(os.path.join(B, "presskit.html"), "w", encoding="utf-8").write(press)
json.dump(strings, open(os.path.join(B, "i18n", "en.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(strings), "строк")
