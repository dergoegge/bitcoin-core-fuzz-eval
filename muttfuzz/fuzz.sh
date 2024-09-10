#!/bin/bash

set -xe

mkdir --parents $REACHABILITY_CORPUS
touch $EVAL_RESULTS

muttfuzz "./bitcoin/build/src/test/fuzz/fuzz" ./bitcoin/build/src/test/fuzz/fuzz \
  --time_per_mutant $TIME_PER_MUTANT \
  --reachability_check_cmd "./bitcoin/build/src/test/fuzz/fuzz -runs=1 $REACHABILITY_CORPUS" \
  --score --avoid_repeats --verbose \
  --budget $EVAL_BUDGET \
  --save_results $EVAL_RESULTS $@
