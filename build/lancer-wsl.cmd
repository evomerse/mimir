@echo off
rem Lance Mimir (build compile sous WSL2) avec son propre profil : ~/.config/mimir/mimir dans WSL.
rem Cette fenetre doit rester ouverte : WSL tue Mimir si la session se ferme.
wsl -d Ubuntu-24.04 -- bash -c "exec $HOME/ff/esr153/obj-validate/dist/bin/mimir"
