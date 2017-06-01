MAIN      = main
SRCS      = *.tex 
PS        = $(MAIN).ps
PDF       = $(MAIN).pdf
DVI       = $(MAIN).dvi
TARG      = $(MAIN).done


all: 
	latex $(MAIN)
	latex $(MAIN)

p: all ps pdf s

s:
	${HOME}/bin/pdfreader main.pdf


$(MAIN).aux: $(MAIN).tex
	source SourceMe ; \
	latex $(MAIN)

#%.ps: %.dvi
#	dvips -o $@ $*
ps:
	dvips -o main.ps main

#%.pdf: %.ps 
#	ps2pdf14 $^
pdf:
	ps2pdf14 main.ps

ds: main.dvi
	dvips -o main.ps main
	gv main.ps &

dd: 
	dvips -o main.ps main
	ps2pdf14 main.ps
	xpdf main.pdf &

cp: 
	cp -f main.ps /u/h/a/haryadi/public/html/script.ps
	cp -f main.pdf /u/h/a/haryadi/public/html/script.pdf

clean:
	rm -f $(PS) $(PDF) $(DVI) $(TARG) *.aux *~ $(MAIN).log $(MAIN).bbl $(MAIN).blg *.pdf *.ps

getps:
	rm -f script.ps
	wget www.cs.wisc.edu/~haryadi/script.ps
	gv script.ps 

getpdf:
	rm -f script.pdf
	wget www.cs.wisc.edu/~haryadi/script.pdf
	acroread script.pdf &

scp:
	scptm \* netapp/talk-slides/script/s0/

.SECONDARY: $(DVI)
