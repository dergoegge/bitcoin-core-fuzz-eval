#!/bin/bash

set -xe

mkdir --parents $REACHABILITY_CORPUS
touch $EVAL_RESULTS
mkdir --parents $LIBFUZZER_WORK_CORPUS

muttfuzz "./bitcoin/build/src/test/fuzz/fuzz -timeout=$LIBFUZZER_TIMEOUT $LIBFUZZER_WORK_CORPUS $SEED_CORPUS" \
  ./bitcoin/build/src/test/fuzz/fuzz \
  --time_per_mutant $TIME_PER_MUTANT \
  --post_mutant_cmd "rm -rf $LIBFUZZER_WORK_CORPUS/ && mkdir --parents $LIBFUZZER_WORK_CORPUS" \
  --reachability_check_cmd "./bitcoin/build/src/test/fuzz/fuzz -runs=1 $REACHABILITY_CORPUS" \
  --score --avoid_repeats --verbose \
  --budget $EVAL_BUDGET \
  --no_timeout_kills \
  --save_results $EVAL_RESULTS $@
