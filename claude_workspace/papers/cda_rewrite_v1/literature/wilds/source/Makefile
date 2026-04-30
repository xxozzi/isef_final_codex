default: 
	pdflatex main
	bibtex main
	open -a preview main.pdf

oldmain: refdb
	pdflatex oldmain
	bibtex oldmain

onepage: refdb
	pdflatex onepage
	bibtex onepage

clean:
	rm main.aux main.log main.out main.bbl main.blg

refdb:
	git clone https://github.com/percyliang/refdb

sfig:
	git clone https://github.com/percyliang/sfig

run:
	go main.pdf
