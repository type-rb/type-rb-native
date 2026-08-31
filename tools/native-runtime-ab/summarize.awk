BEGIN {
	FS = "\t"
	OFS = "\t"
	expected_header = "phase\tround\tretained_index\torder\tcase\tcandidate\tverdict\treturnvalue\texitsignal\tterminationreason\twalltime_seconds\tcputime_seconds\tmemory_bytes"
	if (candidates == "") candidates = "baseline candidate"
	if (retained_rounds == 0) retained_rounds = 11
	candidate_count = split(candidates, candidate_names, " ")
}

NR == 1 {
	if ($0 != expected_header) exit 2
	next
}

{
	if (NF != 13) exit 2
	if (case_name == "") case_name = $5
	if ($5 != case_name) exit 2
	seen[$6] = 1
	if ($1 != "retained") next
	total[$6] += 1
	if ($7 != "pass") next
	passed[$6] += 1
	sample_index = passed[$6]
	wall[$6, sample_index] = $11 + 0
	cpu[$6, sample_index] = $12 + 0
	memory[$6, sample_index] = $13 + 0
}

function metric_value(candidate, metric, sample) {
	if (metric == "wall") return wall[candidate, sample]
	if (metric == "cpu") return cpu[candidate, sample]
	return memory[candidate, sample]
}

function median(candidate, metric, count,    sample, position, value, result) {
	for (sample = 1; sample <= count; sample += 1) {
		value = metric_value(candidate, metric, sample)
		position = sample
		while (position > 1 && sorted[position - 1] > value) {
			sorted[position] = sorted[position - 1]
			position -= 1
		}
		sorted[position] = value
	}
	result = sorted[int((count + 1) / 2)]
	for (sample = 1; sample <= count; sample += 1) delete sorted[sample]
	return result
}

END {
	if (NR < 2) exit 2
	print "case", "candidate", "retained", "passed", "walltime_median_seconds", "cputime_median_seconds", "memory_median_bytes", "status"
	for (candidate_index = 1; candidate_index <= candidate_count; candidate_index += 1) {
		candidate = candidate_names[candidate_index]
		if (!(candidate in seen) || total[candidate] != retained_rounds || passed[candidate] != retained_rounds) {
			print case_name, candidate, total[candidate] + 0, passed[candidate] + 0, "", "", "", "incomplete"
			continue
		}
		print case_name, candidate, total[candidate], passed[candidate], \
			median(candidate, "wall", passed[candidate]), \
			median(candidate, "cpu", passed[candidate]), \
			median(candidate, "memory", passed[candidate]), \
			"pass"
	}
}
