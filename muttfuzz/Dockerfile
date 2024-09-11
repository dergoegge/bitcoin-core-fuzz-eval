# Bitcoin Core fuzz harness evaluation using muttfuzz (https://github.com/agroce/muttfuzz).

FROM debian:sid-slim

RUN apt update && apt upgrade -y && \
  apt install -y python3 python3-pip python3-venv \
  lsb-release wget software-properties-common gnupg \
  git \
  build-essential libtool autotools-dev automake pkg-config bsdmainutils cmake \
  libevent-dev libboost-dev libsqlite3-dev \
  ccache \
  vim

ARG LLVM_VERSION=18
RUN wget https://apt.llvm.org/llvm.sh && chmod +x llvm.sh
RUN ./llvm.sh $LLVM_VERSION all

ARG OWNER=bitcoin
ARG REPO=bitcoin
ARG BRANCH=master
RUN git clone --branch $BRANCH https://github.com/$OWNER/$REPO.git

# Build Bitcoin Core's fuzz binary
ENV CC clang-$LLVM_VERSION
ENV CXX clang++-$LLVM_VERSION
ENV LDFLAGS "-fuse-ld=lld"
ENV CCACHE_DIR /ccache/

RUN --mount=type=cache,target=/ccache/ \
  cd bitcoin && \
  cmake -B build/ \
    -DCMAKE_C_COMPILER=$CC \
    -DCMAKE_CXX_COMPILER=$CXX \
    -DBUILD_FOR_FUZZING=ON \
    -DSANITIZERS=fuzzer && \
  cmake --build build/ -j$(nproc)

# Install muttfuzz
ENV VIRTUAL_ENV /opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH "$VIRTUAL_ENV/bin:$PATH"

RUN pip3 install muttfuzz

ARG HARNESS
ENV FUZZ $HARNESS

# How long to fuzz each mutant in seconds
ARG TIME_PER_MUTANT=300
ENV TIME_PER_MUTANT $TIME_PER_MUTANT
# Per input fuzz timeout for libfuzzer
ARG LIBFUZZER_TIMEOUT=5
ENV LIBFUZZER_TIMEOUT $LIBFUZZER_TIMEOUT
# Total duration for evaluation
ARG EVAL_BUDGET=3600
ENV EVAL_BUDGET $EVAL_BUDGET

# Corpus used to determine mutant reachability
ARG REACHABILITY_CORPUS=/share/corpus
ENV REACHABILITY_CORPUS $REACHABILITY_CORPUS
# Seed corpus used for fuzzing the mutants (new find are erased between mutants)
ARG SEED_CORPUS=$REACHABILITY_CORPUS
ENV SEED_CORPUS $SEED_CORPUS
# Location to store muttfuzz results (to be processed by `crunch_results.py`)
ARG EVAL_RESULTS=/share/results.csv
ENV EVAL_RESULTS $EVAL_RESULTS

ENV LIBFUZZER_WORK_CORPUS /tmp/work-corpus

COPY ./fuzz.sh .
ENTRYPOINT [ "./fuzz.sh" ]
