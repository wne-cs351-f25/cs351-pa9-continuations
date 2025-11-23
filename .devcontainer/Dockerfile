FROM node:20

# Install basic tools and Python build dependencies
RUN apt-get update && \
    apt-get install -y \
        less \
        git \
        procps \
        sudo \
        fzf \
        zsh \
        man-db \
        unzip \
        gnupg2 \
        gh \
        aggregate \
        jq \
        nano \
        vim \
        g++ \
        gcc \
        make \
        valgrind \
        time \
        build-essential \
        libssl-dev \
        zlib1g-dev \
        libbz2-dev \
        libreadline-dev \
        libsqlite3-dev \
        wget \
        curl \
        llvm \
        libncurses5-dev \
        libncursesw5-dev \
        xz-utils \
        tk-dev \
        libffi-dev \
        liblzma-dev \
        python3-openssl \
        && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
    
# Install AI agents
RUN npm install -g @anthropic-ai/claude-code
RUN npm install -g @google/gemini-cli
RUN npm install -g @openai/codex
RUN npm install -g @githubnext/github-copilot-cli
RUN npm install -g @intellectronica/ruler

# Build Python 3.13.0 with --disable-gil (Free Threading)
# Installing to /opt/python-3.13t
RUN cd /tmp && \
    wget https://www.python.org/ftp/python/3.13.0/Python-3.13.0.tgz && \
    tar xvf Python-3.13.0.tgz && \
    cd Python-3.13.0 && \
    ./configure --disable-gil --prefix=/opt/python-3.13t && \
    make -j$(nproc) && \
    make install && \
    cd .. && \
    rm -rf Python-3.13.0 Python-3.13.0.tgz

# Create a global symlink 'python-free' for easier access
RUN ln -s /opt/python-3.13t/bin/python3.13 /usr/local/bin/python-free

ENV PLCC_GIT_BRANCH=main

USER node
