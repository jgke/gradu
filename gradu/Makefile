FILES=gradu.tex johdanto.tex maaritelmat.tex muut.tex oma.tex yhteenveto.tex liite.tex \
      references.bib \
      gradu.sty tktltiki.cls \
      unnumberedtotoc.sty xassoccnt.sty

TARGET=gradu.pdf

TEX="pdflatex --shell-escape --halt-on-error"

all: ${TARGET}
${TARGET}: ${FILES}
	${TEX} gradu.tex
	bibtex gradu
	${TEX} gradu.tex
	${TEX} gradu.tex
	${TEX} gradu.tex

.PHONY: watch
watch:
	texbuild gradu.tex ${FILES}
