# Temporal trend task

Serve this directory with `python -m http.server 8000 --bind 127.0.0.1` and open `temporal-task.html` in a browser through your normal development hosting setup. HTTP serving is required to load the CSV manifests.

The original `task.html` remains unchanged. This second task loads `manifest.csv` and `manifest_training.csv` directly, without PNG stimuli or the local `stimuli2` links. For each trial, it pairs `x_values` with `y_values`, sorts by X, and presents the Y values in that order. All dots share the screen's horizontal center. Vertical placement uses the generator's fixed Y range [-0.27, 1.27] and canvas margins. Dot diameter comes from `dot_size_px`.

Each dot is shown for a nominal 200 ms, replaced immediately by the next dot without an intentional blank interval. X determines presentation order; adjacent X values in the supplied manifests are equally spaced. Sequences last approximately 1.6–4.4 seconds for 8–22 dots. Browser rendering can extend these durations; actual dot onsets and total sequence duration are recorded. This is browser timing, not a guarantee of laboratory-grade 200 ms exposures.

Participants respond only after the entire sequence. There is no neutral comparison array: participants judge the temporal trend itself. Reaction time is measured from sequence completion; time from sequence start is also recorded. Switching tabs pauses the task and replays an interrupted, unanswered sequence on continuation.

There are 10 randomly selected practice trials followed by all 512 main stimuli without replacement. Breaks occur after 128, 256, and 384 main trials. Three or more wrong answers in the last six responses trigger a reminder; a due break follows the reminder.

`C=1` or `C=2` maps Q to increasing and P to decreasing. `C=3` or `C=4` reverses the mapping. Without a valid C, the mapping is randomly selected. Every condition is trend-only. Optional `id` and `ResponseID` URL parameters are included in the CSV.

Responses are retained in memory, with a download link available on instruction/break screens after the first response and at completion. Reloading or closing the page loses undownloaded responses. This task does not submit data to jsPsych Pipe or signal Qualtrics completion. A separate experiment destination and integration should be configured before deploying it as a live study.
