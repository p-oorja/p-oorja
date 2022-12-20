# FROM python:3.9-slim-buster

# ENV PYTHONUNBUFFERED 1
# ENV PYTHONDONTWRITEBYTECODE 1

# RUN apt-get update \
#   # dependencies for building Python packages
#   && apt-get install -y build-essential \
#   # psycopg2 dependencies
#   && apt-get install -y libpq-dev \
#   # Additional dependencies
#   && apt-get install -y telnet netcat curl \
#   # cleaning up unused files
#   && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
#   && rm -rf /var/lib/apt/lists/*

FROM debian:latest

# Getting GCC-9
RUN echo 'deb http://deb.debian.org/debian testing main' >> /etc/apt/sources.list
RUN apt update -y
RUN apt install -y gcc


 # psycopg2 dependencies
RUN apt install -y libpq-dev

RUN apt install -y wget
RUN apt install -y curl
###Setiting up python
# ensure local python is preferred over distribution python

RUN apt install -qq -y -t testing build-essential

RUN apt-get install -qq -y libssl-dev zlib1g-dev \
  libbz2-dev libreadline-dev libsqlite3-dev llvm \
  libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev

ENV PATH /usr/local/bin:$PATH

# http://bugs.python.org/issue19846
# > At the moment, setting "LANG=C" on a Linux system *fundamentally breaks Python 3*, and that's not OK.
ENV LANG C.UTF-8

# runtime dependencies
RUN set -eux; \
	apt-get update; \
	apt-get install -y --no-install-recommends \
		libbluetooth-dev \
		tk-dev \
		uuid-dev \
	; \
	rm -rf /var/lib/apt/lists/*

ENV GPG_KEY E3FF2839C048B25C084DEBE9B26995E310250568
ENV PYTHON_VERSION 3.9.15

RUN set -eux; \
	\
	wget -O python.tar.xz "https://www.python.org/ftp/python/${PYTHON_VERSION%%[a-z]*}/Python-$PYTHON_VERSION.tar.xz"; \
	wget -O python.tar.xz.asc "https://www.python.org/ftp/python/${PYTHON_VERSION%%[a-z]*}/Python-$PYTHON_VERSION.tar.xz.asc"; \
	GNUPGHOME="$(mktemp -d)"; export GNUPGHOME; \
	gpg --batch --keyserver hkps://keys.openpgp.org --recv-keys "$GPG_KEY"; \
	gpg --batch --verify python.tar.xz.asc python.tar.xz; \
	command -v gpgconf > /dev/null && gpgconf --kill all || :; \
	rm -rf "$GNUPGHOME" python.tar.xz.asc; \
	mkdir -p /usr/src/python; \
	tar --extract --directory /usr/src/python --strip-components=1 --file python.tar.xz; \
	rm python.tar.xz; \
	\
	cd /usr/src/python; \
	gnuArch="$(dpkg-architecture --query DEB_BUILD_GNU_TYPE)"; \
	./configure \
		--build="$gnuArch" \
		--enable-loadable-sqlite-extensions \
		--enable-optimizations \
		--enable-option-checking=fatal \
		--enable-shared \
		--with-system-expat \
		--without-ensurepip \
	; \
	nproc="$(nproc)"; \
	make -j "$nproc" \
	; \
	make install; \
	\
# enable GDB to load debugging data: https://github.com/docker-library/python/pull/701
	bin="$(readlink -ve /usr/local/bin/python3)"; \
	dir="$(dirname "$bin")"; \
	mkdir -p "/usr/share/gdb/auto-load/$dir"; \
	cp -vL Tools/gdb/libpython.py "/usr/share/gdb/auto-load/$bin-gdb.py"; \
	\
	cd /; \
	rm -rf /usr/src/python; \
	\
	find /usr/local -depth \
		\( \
			\( -type d -a \( -name test -o -name tests -o -name idle_test \) \) \
			-o \( -type f -a \( -name '*.pyc' -o -name '*.pyo' -o -name 'libpython*.a' \) \) \
		\) -exec rm -rf '{}' + \
	; \
	\
	ldconfig; \
	\
	python3 --version

# make some useful symlinks that are expected to exist ("/usr/local/bin/python" and friends)
RUN set -eux; \
	for src in idle3 pydoc3 python3 python3-config; do \
		dst="$(echo "$src" | tr -d 3)"; \
		[ -s "/usr/local/bin/$src" ]; \
		[ ! -e "/usr/local/bin/$dst" ]; \
		ln -svT "$src" "/usr/local/bin/$dst"; \
	done

# if this is called "PIP_VERSION", pip explodes with "ValueError: invalid truth value '<VERSION>'"
ENV PYTHON_PIP_VERSION 22.0.4
# https://github.com/docker-library/python/issues/365
ENV PYTHON_SETUPTOOLS_VERSION 58.1.0
# https://github.com/pypa/get-pip
ENV PYTHON_GET_PIP_URL https://github.com/pypa/get-pip/raw/66030fa03382b4914d4c4d0896961a0bdeeeb274/public/get-pip.py
ENV PYTHON_GET_PIP_SHA256 1e501cf004eac1b7eb1f97266d28f995ae835d30250bec7f8850562703067dc6

RUN set -eux; \
	\
	wget -O get-pip.py "$PYTHON_GET_PIP_URL"; \
	echo "$PYTHON_GET_PIP_SHA256 *get-pip.py" | sha256sum -c -; \
	\
	export PYTHONDONTWRITEBYTECODE=1; \
	\
	python get-pip.py \
		--disable-pip-version-check \
		--no-cache-dir \
		--no-compile \
		"pip==$PYTHON_PIP_VERSION" \
		"setuptools==$PYTHON_SETUPTOOLS_VERSION" \
	; \
	rm -f get-pip.py; \
	\
	pip --version


# Requirements are installed here to ensure they will be cached.
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt


ENV JULIA_PATH /usr/local/julia
ENV PATH $JULIA_PATH/bin:$PATH

# https://julialang.org/juliareleases.asc
# Julia (Binary signing key) <buildbot@julialang.org>
ENV JULIA_GPG 3673DF529D9049477F76B37566E3C7DC03D6E495

# https://julialang.org/downloads/
ENV JULIA_VERSION 1.9.0-alpha1

RUN set -eux; \
	\
	savedAptMark="$(apt-mark showmanual)"; \
	if ! command -v gpg > /dev/null; then \
		apt-get update; \
		apt-get install -y --no-install-recommends \
			gnupg \
			dirmngr \
		; \
		rm -rf /var/lib/apt/lists/*; \
	fi; \
	\
# https://julialang.org/downloads/#julia-command-line-version
# https://julialang-s3.julialang.org/bin/checksums/julia-1.9.0-alpha1.sha256
	arch="$(dpkg --print-architecture)"; \
	case "$arch" in \
		'amd64') \
			url='https://julialang-s3.julialang.org/bin/linux/x64/1.9/julia-1.9.0-alpha1-linux-x86_64.tar.gz'; \
			sha256='c657ed4e792f300d45d1ea5ffb71d052cae4e0d653142b277a3cba4d2cecfd7d'; \
			;; \
		'arm64') \
			url='https://julialang-s3.julialang.org/bin/linux/aarch64/1.9/julia-1.9.0-alpha1-linux-aarch64.tar.gz'; \
			sha256='595451736674c8f2e1cd8be514901cf47043ffc611078c1edcca7d7901ffafb8'; \
			;; \
		'i386') \
			url='https://julialang-s3.julialang.org/bin/linux/x86/1.9/julia-1.9.0-alpha1-linux-i686.tar.gz'; \
			sha256='c8b9312e9b210974a26e9abe3a6d70be9e30f1603a227a11bb2ce1c62351df07'; \
			;; \
		*) \
			echo >&2 "error: current architecture ($arch) does not have a corresponding Julia binary release"; \
			exit 1; \
			;; \
	esac; \
	\
	curl -fL -o julia.tar.gz.asc "$url.asc"; \
	curl -fL -o julia.tar.gz "$url"; \
	\
	echo "$sha256 *julia.tar.gz" | sha256sum --strict --check -; \
	\
	export GNUPGHOME="$(mktemp -d)"; \
	gpg --batch --keyserver keyserver.ubuntu.com --recv-keys "$JULIA_GPG"; \
	gpg --batch --verify julia.tar.gz.asc julia.tar.gz; \
	command -v gpgconf > /dev/null && gpgconf --kill all; \
	rm -rf "$GNUPGHOME" julia.tar.gz.asc; \
	\
	mkdir "$JULIA_PATH"; \
	tar -xzf julia.tar.gz -C "$JULIA_PATH" --strip-components 1; \
	rm julia.tar.gz; \
	\
	apt-mark auto '.*' > /dev/null; \
	[ -z "$savedAptMark" ] || apt-mark manual $savedAptMark; \
	apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false; \
	\
# smoke test
	julia --version

COPY install.jl /install.jl
RUN julia /install.jl

RUN apt update -y
RUN apt-get -o Dpkg::Options::="--force-confmiss" install -y --reinstall netbase

COPY ./compose/local/flask/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

COPY ./compose/local/flask/celery/worker/start /start-celeryworker
RUN sed -i 's/\r$//g' /start-celeryworker
RUN chmod +x /start-celeryworker

COPY ./compose/local/flask/celery/beat/start /start-celerybeat
RUN sed -i 's/\r$//g' /start-celerybeat
RUN chmod +x /start-celerybeat

WORKDIR /app

#ENTRYPOINT ["/start"]
