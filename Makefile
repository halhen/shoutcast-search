#shoutcast-search - search shoutcast.com radio stations

include config.mk

install:
	@echo installing executable file to ${DESTDIR}${PREFIX}/bin
	@mkdir -p ${DESTDIR}${PREFIX}/bin
	@cp -f shoutcast-search ${DESTDIR}${PREFIX}/bin
	@chmod 755 ${DESTDIR}${PREFIX}/bin/shoutcast-search
	@echo installing shoutcast_search Python library
	@python setup.py install --prefix=${PREFIX} --root=${DESTDIR}
	@echo installing manual page to ${DESTDIR}${MANPREFIX}/man1
	@mkdir -p ${DESTDIR}${MANPREFIX}/man1
	@cp -f shoutcast-search.1 ${DESTDIR}${MANPREFIX}/man1/shoutcast-search.1
	@chmod 644 ${DESTDIR}${MANPREFIX}/man1/shoutcast-search.1

uninstall:
	@echo removing executable file from ${DESTDIR}${PREFIX}/bin
	@rm ${DESTDIR}${PREFIX}/bin/shoutcast-search
	@echo removing manual page from ${DESTDIR}${MANPREFIX}/bin
	@rm ${DESTDIR}${MANPREFIX}/man1/shoutcast-search.1
