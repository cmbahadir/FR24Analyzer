FROM alpine:latest


# ############
# unprivileged
# ############

# explicitly set user/group IDs
# RUN addgroup -r unprivileged --gid=999 && adduser -m -r -g unprivileged --uid=999 unprivileged
RUN addgroup unprivileged -g 998 && adduser unprivileged -D -G unprivileged

# grab gosu for easy step-down from root
ENV GOSU_VERSION 1.11
RUN set -eux; \
	\
	apk add --no-cache --virtual .gosu-deps \
		ca-certificates \
		dpkg \
		gnupg \
	; \
	\
	dpkgArch="$(dpkg --print-architecture | awk -F- '{ print $NF }')"; \
	wget -O /usr/local/bin/gosu "https://github.com/tianon/gosu/releases/download/$GOSU_VERSION/gosu-$dpkgArch"; \
	wget -O /usr/local/bin/gosu.asc "https://github.com/tianon/gosu/releases/download/$GOSU_VERSION/gosu-$dpkgArch.asc"; \
	\
# verify the signature
	export GNUPGHOME="$(mktemp -d)"; \
	gpg --batch --keyserver hkps://keys.openpgp.org --recv-keys B42F6819007F00F88E364FD4036A9C25BF357DD4; \
	gpg --batch --verify /usr/local/bin/gosu.asc /usr/local/bin/gosu; \
	command -v gpgconf && gpgconf --kill all || :; \
	rm -rf "$GNUPGHOME" /usr/local/bin/gosu.asc; \
	\
# clean up fetch dependencies
	apk del --no-network .gosu-deps; \
	\
	chmod +x /usr/local/bin/gosu; \
# verify that the binary works
	gosu --version; \
	gosu nobody true


# PATHS
ENV PYTHON_PATH=/usr/local/bin/ \
    PATH="/usr/local/lib/python$PYTHON_VERSION/bin/:/usr/local/lib/pyenv/versions/$PYTHON_VERSION/bin:${PATH}" \
    # These are always installed.
    #   * dumb-init: a proper init system for containers, to reap zombie children
    #   * musl: standard C library
    #   * lib6-compat: compatibility libraries for glibc
    #   * linux-headers: commonly needed, and an unusual package name from Alpine.
    #   * build-base: used so we include the basic development packages (gcc)
    #   * bash: so we can access /bin/bash
    #   * git: to ease up clones of repos
    #   * ca-certificates: for SSL verification during Pip and easy_install
    PACKAGES="\
      dumb-init \
      musl \
      libc6-compat \
      linux-headers \
      build-base \
      bash \
      git \
      ca-certificates \
      libssl1.0 \
      libffi-dev \
      tzdata \
    " \
    # PACKAGES needed to built python
    PYTHON_BUILD_PACKAGES="\
      bzip2-dev \
      coreutils \
      dpkg-dev dpkg \
      expat-dev \
      findutils \
      gcc \
      gdbm-dev \
      libc-dev \
      libffi-dev \
      libnsl-dev \
      libtirpc-dev \
      linux-headers \
      make \
      ncurses-dev \
      libressl-dev \
      pax-utils \
      readline-dev \
      sqlite-dev \
      tcl-dev \
      tk \
      tk-dev \
      util-linux-dev \
      xz-dev \
      zlib-dev \
      git \
	  libressl2.7-libcrypto \
    "

RUN set -ex ;\
    # find MAJOR and MINOR python versions based on $PYTHON_VERSION
    export PYTHON_MAJOR_VERSION=$(echo "${PYTHON_VERSION}" | rev | cut -d"." -f3-  | rev) ;\
    export PYTHON_MINOR_VERSION=$(echo "${PYTHON_VERSION}" | rev | cut -d"." -f2-  | rev) ;\
    # replacing default repositories with edge ones
    echo "http://dl-cdn.alpinelinux.org/alpine/v$ALPINE_VERSION/community" >> /etc/apk/repositories ;\
    echo "http://dl-cdn.alpinelinux.org/alpine/v$ALPINE_VERSION/main" >> /etc/apk/repositories ;\
    # Add the packages, with a CDN-breakage fallback if needed
    apk add --no-cache $PACKAGES || \
        (sed -i -e 's/dl-cdn/dl-4/g' /etc/apk/repositories && apk add --no-cache $PACKAGES) ;\
    # Add packages just for the python build process with a CDN-breakage fallback if needed
    apk add --no-cache --virtual .build-deps $PYTHON_BUILD_PACKAGES || \
        (sed -i -e 's/dl-cdn/dl-4/g' /etc/apk/repositories && apk add --no-cache --virtual .build-deps $PYTHON_BUILD_PACKAGES) ;\
    # turn back the clock -- so hacky!
    echo "http://dl-cdn.alpinelinux.org/alpine/v$ALPINE_VERSION/main/" > /etc/apk/repositories ;\
    # echo "@community http://dl-cdn.alpinelinux.org/alpine/v$ALPINE_VERSION/community" >> /etc/apk/repositories ;\
    # echo "@testing http://dl-cdn.alpinelinux.org/alpine/v$ALPINE_VERSION/testing" >> /etc/apk/repositories ;\
    # echo "@edge-main http://dl-cdn.alpinelinux.org/alpine/edge/main" >> /etc/apk/repositories ;\
    # use pyenv to download and compile specific python version
    git clone --depth 1 https://github.com/pyenv/pyenv /usr/local/lib/pyenv ;\
    # install
    GNU_ARCH="$(dpkg-architecture --query DEB_BUILD_GNU_TYPE)" ;\
    # flag explanation:
    # --with-shared : python-dev
    PYENV_ROOT=/usr/local/lib/pyenv CONFIGURE_OPTS="--build=$GNU_ARCH --enable-loadable-sqlite-extensions --enable-shared --with-system-expat --with-system-ffi --without-ensurepip --with-shared" /usr/local/lib/pyenv/bin/pyenv install $PYTHON_VERSION ;\
    # keep the needed .so files
    # ignore libpython - that one comes from the pyenv instalation
    find /usr/local -type f -executable -not \( -name '*tkinter*' \) -exec scanelf --needed --nobanner --format '%n#p' '{}' ';' \
        | tr ',' '\n' \
        | sort -u \
        | awk 'system("[ -e /usr/local/lib/" $1 " ]") == 0 { next } { print "so:" $1 }' \
        | grep -ve 'libpython' \
        | xargs -rt apk add --no-cache --virtual .python-rundeps ;\
        # for debug
        # | xargs -n1 echo ;\
    # delete everything from pyenv except the installed version
    # this throws an error but we ignore it
    find /usr/local/lib/pyenv/ -mindepth 1 -name versions -prune -o -exec rm -rf {} \; || true ;\
    # delete files to to reduce container size
    # tips taken from main python docker repo
    find /usr/local/lib/pyenv/versions/$PYTHON_VERSION/ -depth \( -name '*.pyo' -o -name '*.pyc' -o -name 'test' -o -name 'tests' \) -exec rm -rf '{}' + ;\
    # symlink the binaries
    ln -s /usr/local/lib/pyenv/versions/$PYTHON_VERSION/bin/* $PYTHON_PATH ;\
    # set timezone info
    ln -fs /usr/share/zoneinfo/Etc/UTC /etc/localtime ;\
    # remove build dependencies and any leftover apk cache
    apk del --no-cache --purge .build-deps ;\
    rm -rf /var/cache/apk/*

# since we will be "always" mounting the volume, we can set this up
ENTRYPOINT ["/usr/bin/dumb-init"]
CMD ["python"]

# #######
# PROJECT
# #######

ENV PYTHONUNBUFFERED 1

# RUN mkdir -p /app /static /media /cache && chown -R unprivileged:unprivileged /media /cache
WORKDIR /app

COPY requirements.txt /requirements.txt
COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN pip3 install --no-cache-dir -r /requirements.txt

# ENV STATIC_ROOT /static
# ENV MEDIA_DIR /media
# ENV DATA_DIR /cache

COPY . /app
# RUN /app/docker-prepare.sh

EXPOSE 8000
VOLUME ["/app"]
ENTRYPOINT ["/docker-entrypoint.sh"]