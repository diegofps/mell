#!/usr/bin/env bash

mell en     --output output/en     --clean && (cd output/en     && xelatex resume.tex && xdg-open resume.pdf) &
mell pt     --output output/pt     --clean && (cd output/pt     && xelatex resume.tex && xdg-open resume.pdf) &
mell nubank --output output/nubank --clean && (cd output/nubank && xelatex resume.tex && xdg-open resume.pdf) &
mell apple  --output output/apple  --clean && (cd output/apple  && xelatex resume.tex && xdg-open resume.pdf) &

wait
