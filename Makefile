MAIN      = main
SRCS      = *.tex 
PS        = $(MAIN).ps
PDF       = $(MAIN).pdf
DVI       = $(MAIN).dvi
TARG      = $(MAIN).done



#all: texwithredo cleanabit
all: texnoredo cleanabit


p: all ps pdf s cleanabit

s:
	${HOME}/bin/skim main.pdf

texwithredo:
	latex main.tex
	bibtex -min-crossrefs=100 main
	${HOME}/bin/redo-bib.csh main
	latex main.tex
	latex main.tex

texnoredo:
	latex main.tex
	bibtex -min-crossrefs=100 main
	latex main.tex
	latex main.tex

texnobib:
	latex main.tex
	latex main.tex


$(MAIN).bbl: $(MAIN).aux
	bibtex -min-crossrefs=100 $(MAIN)
	./redo-bib.csh $(MAIN)

x:
	xdvi -bg gray main.dvi &


$(MAIN).aux: $(MAIN).tex
	latex $(MAIN)

ps: $(DVI)
	dvips -o $(PS) $(MAIN)

pdf: $(PS)
	ps2pdf14 $(PS)

cps:
	cp main.ps /u/h/a/haryadi/public/html/main.ps

cpf:
	cp main.pdf /u/h/a/haryadi/public/html/main.pdf

clean:
	rm -vf *.ps  main.pdf *.dvi *.aux *.log \
	*.bbl *.blg *.out *.brf *.4*  \
  *.lot *.lof *.toc \
	*.css *.idv *.lg *.tmp *.xref *.png

cleanabit:
	rm -vf *~ *.ps  *.aux *.log \
	*.bbl *.blg *.out *.brf *.4*  \
	*.css *.idv *.lg *.tmp *.xref *.png


