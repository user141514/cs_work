# Invalid manipulation attempt

The first Original-TP Luna/Medium manipulation call is excluded from scientific interpretation.

Reason: the multiline prompt was passed as a Windows command-line argument through `codex.cmd`; the Codex log shows only the header/instruction paragraph arrived, while the frozen Success Case and Ongoing task were absent. The model therefore asked the user to provide the cases.

Classification: INVALID_TRANSPORT, not a negative result for Original TP or OI-TP.

Correction: both valid arms must use the same `codex exec -` stdin transport.
