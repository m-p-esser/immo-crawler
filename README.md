# Plattforms

"Portal","Besonderheiten"
"Immowelt","https://www.immoxxl.de/blog/immobilienportale"
"Immonet","https://www.immoxxl.de/blog/immobilienportale"
"Wunschimmo.de","https://www.immoxxl.de/blog/immobilienportale"
"Immobilien.de","https://www.immoxxl.de/blog/immobilienportale"
"Wohnungsboerse.net","https://www.similarweb.com/website/immobilienscout24.de/competitors/"
"Immosuchmaschine.de","https://www.similarweb.com/website/immobilienscout24.de/competitors/"
"wg-gesucht.de","https://www.similarweb.com/website/immobilienscout24.de/competitors/"
"ohne-makler.net","https://www.similarweb.com/website/immobilienscout24.de/competitors/"
"immobilo.de","https://www.similarweb.com/website/immobilienscout24.de/competitors/"

## Roadmap
- [x] Create Branch release-prod
- [x] Create Branch release-test
    - [x] Set release-test as default branch
- Clone Github Repo before running Airflow Jobs
- Add pagination to Immowelt BS4 Crawler


## Setup Airflow VM
- Install GIT: `sudo apt install git`
- Create SSH Key on VM: `ssh-keygen -t ed25519 -C "your_email@example.com"`
- Clone Repo
- Run setup-airflow-vm.sh
