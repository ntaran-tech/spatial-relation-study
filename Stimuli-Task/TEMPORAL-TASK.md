# Temporal trend task

Serve this directory with `python -m http.server 8000 --bind 127.0.0.1` and open `temporal-task.html` through your normal development hosting setup. HTTP serving is required to load CSV manifests. On GitHub Pages the task is at `Stimuli-Task/temporal-task.html`.

The current bank is [Ciccione-stimuli](Ciccione-stimuli/README.md), based on Experiment 1 of Ciccione & Dehaene (2021). It contains 672 main trials in six blocks of 112 and 25 practice trials. That document details the generation method, seed, and adaptations. The original `task.html` and original manifests remain unchanged.

For each trial, the temporal task pairs `x_values` with `y_values`, sorts by X, and presents Y values in that order. All dots share the screen's horizontal center. Vertical placement uses the fixed Y range [-0.27, 1.27] and original canvas margins. Dot diameter comes from `dot_size_px`.

Each dot is shown for nominally 200 ms, replaced immediately by the next dot without an intentional blank interval. X determines presentation order; adjacent X values are equally spaced. Sequences last about 1.2–13.2 seconds for 6–66 dots. Main sequences alone total about 72 minutes. Browser rendering can extend durations; actual dot onsets and total sequence duration are recorded.

Participants respond only after the entire sequence. They judge the temporal trend itself, without a neutral comparison array. Reaction time starts at sequence completion; time from sequence start is also recorded. Switching tabs pauses the task and replays an interrupted unanswered sequence on continuation.

Each main block contains all 112 combinations once, shuffled within block. Three or more wrong answers in the last six responses trigger a reminder; a due break follows it. A centered square shows green for correct or red for incorrect for 500 ms after each response. Feedback is based on the observed OLS trend, including zero prescribed slopes and sign reversals caused by noise.

`C=1` or `C=2` maps Q to increasing and P to decreasing. `C=3` or `C=4` reverses the mapping. Without a valid C, the mapping is randomly selected. Every condition is trend-only. Optional `id` and `ResponseID` URL parameters are included in the CSV.

Responses are retained in memory, with a download link available on instruction/break screens after the first response and at completion. Reloading or closing the page loses undownloaded responses. Exports identify the stimulus set, stimulus index, block, prescribed slope/category, actual slope, and feedback basis. This task does not submit data to jsPsych Pipe or signal Qualtrics completion.
