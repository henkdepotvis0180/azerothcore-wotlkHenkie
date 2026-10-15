# AzerothCore Solo Funserver — moduleoverzicht

Dit is een voorgestelde moduleconfiguratie, **geen bewijs dat de server werkt**.

| Module | Bron | Vastgepinde commit | Status |
| --- | --- | --- | --- |
| Playerbots | https://github.com/mod-playerbots/mod-playerbots | 79bd428115c8f33b74b13de23b133d49c3f75c60 | Basis; build nog verifiëren |

## Codex-gebruik

Vraag bijvoorbeeld: "Voeg mod-transmog toe. Controleer of die samengaat met Playerbots, pin een commit, werk de modulemanifest en dit overzicht bij, en laat de Windows-build controleren."

Codex kan broncode en GitHub-workflows aanpassen. Het kan geen complete werkende gameserver garanderen zonder een succesvolle build, databaseconfiguratie, clientdata en in-game tests.

## Hoe werkt de installatie?

De enige configuratiebron is funserver/modules.json. Het script scripts/funserver_modules.py haalt die repositoryversies op in modules/. Die modulemap is in AzerothCore standaard gitignored, zodat externe modulecode niet per ongeluk in de core-fork wordt gecommit.

De bestaande Windows GitHub Action draait daarna de reguliere AzerothCore-build, inclusief de geïnstalleerde modules. CMake blijft een interne bouwstap, niet een handmatig commando voor de gebruiker.

## Nieuwe modules

Voeg modules één voor één toe en test de eerdere combinatie na iedere toevoeging. Bewaar wijzigingen in modulecode in een eigen fork van de betreffende module, niet in een lokaal genegeerde map.
