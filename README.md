# SabantuyCTF 2021

Task sources & writeups from SabantuyCTF 2021 by C4T BuT S4D and Hackerdom.

## Tasks

Tasks are stored in the [tasks](./tasks) directory. 

The task folder structure is:

- `README.md` contains all information about the task:
  - Header contains task info in form `<difficulty> | <category> | <task_name>`
  - `Description` section contains the public task description
  - `Deploy` section contains author's notes about deploy (more on that below)
  - `Solution` section contains a writeup info
  - `Flag` section contains the flag for this task

- `deploy` folder contains all files necessary to host a task. It **always** contains a `docker-compose.yml` file
- `public` folder contains all files that are to be given to participants
- `dev` folder contains all development files (not really needed, just in case)


| Difficulty | Name | Category | Автор |
|-----------|------|-----------|-------|
| [easy](tasks/easy) | [**Simple cipher**](tasks/easy/crypto-simple-cipher) | Crypto | [@keltecc](https://github.com/keltecc) |
| [easy](tasks/easy) | [**Flag eater**](tasks/easy/flag-eater) | Reverse | [@revervand](https://github.com/revervand) |
| [easy](tasks/easy) | [**Quiz**](tasks/easy/joy-quiz) | Joy | [@keltecc](https://github.com/keltecc) |
| [easy](tasks/easy) | [**Puzzle**](tasks/easy/puzzle) | Joy | [@revervand](https://github.com/revervand) |
| [easy](tasks/easy) | [**Super trace**](tasks/easy/super-trace) | Forensics | [@revervand](https://github.com/revervand) |
| [easy](tasks/easy) | [**Shops site**](tasks/easy/web-sqlstats) | Web | [@jnovikov](https://github.com/jnovikov) |
| [medium](tasks/medium) | [**Periodic**](tasks/medium/admin-periodic) | Admin | [@keltecc](https://github.com/keltecc) |
| [medium](tasks/medium) | [**MDot**](tasks/medium/mdot) | PPC | [@renbou](https://github.com/renbou) |
| [medium](tasks/medium) | [**Book**](tasks/medium/stegano+crypto-book) | Stego, Crypto | [@keltecc](https://github.com/keltecc) |
| [medium](tasks/medium) | [**Bliss**](tasks/medium/stegano-bliss) | Stegano | [@keltecc](https://github.com/keltecc) |
| [medium](tasks/medium) | [**Hide and Seek**](tasks/medium/web+stegano-php) | Web, Stego | [@jnovikov](https://github.com/jnovikov) |
| [medium](tasks/medium) | [**CORSBypasser**](tasks/medium/web-corsbypasser) | Web | [@renbou](https://github.com/renbou) |
| [hard](tasks/hard) | [**Backdoored**](tasks/hard/backdoored) | Forensics | [@revervand](https://github.com/revervand) |
| [hard](tasks/hard) | [**Erawlam**](tasks/hard/erawlam) | Reverse | [@revervand](https://github.com/revervand) |
| [hard](tasks/hard) | [**Vaccinated**](tasks/hard/web+ppc-vaccinated) | Web, PPC | [@jnovikov](https://github.com/jnovikov) |
