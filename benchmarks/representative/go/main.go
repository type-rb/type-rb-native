// Portable controls use the same inputs, outputs and lifetime requirements.
package main

import (
	"encoding/json"
	"fmt"
	"os"
	"slices"
	"strconv"
	"strings"
	"unicode/utf8"
)

func text(length int) string  { return strings.Repeat("aβ😀", length) }
func size(value string) int64 { return int64(utf8.RuneCountInString(value)) }

func logInput(count int, variant string) []string {
	lines := make([]string, 0, count)
	for index := 0; index < count; index++ {
		if variant == "mixed" && index%17 == 0 {
			lines = append(lines, "malformed")
		} else {
			lines = append(lines, "event\tgroup-"+strconv.Itoa(index%127)+"\t"+strconv.Itoa(index%1000)+"\t"+strconv.Itoa(index))
		}
	}
	return lines
}

func aggregateLogs(lines []string) int64 {
	totals := make(map[string]int64)
	var rejected int64
	for _, line := range lines {
		fields := strings.Split(line, "\t")
		if len(fields) != 4 {
			rejected++
			continue
		}
		value, err := strconv.ParseInt(fields[2], 10, 64)
		if err != nil {
			panic(err)
		}
		totals[fields[1]] += value
	}
	keys := make([]string, 0, len(totals))
	for key := range totals {
		keys = append(keys, key)
	}
	slices.Sort(keys)
	output := make([]string, 0, len(keys))
	for _, key := range keys {
		output = append(output, key+"="+strconv.FormatInt(totals[key], 10))
	}
	return size(strings.Join(output, "\n")) + rejected
}

func jsonInput(count int, variant string) []string {
	documents := make([]string, 0, count)
	for index := 0; index < count; index++ {
		if variant == "mixed" && index%17 == 0 {
			documents = append(documents, "{invalid")
		} else {
			documents = append(documents, "{\"id\":"+strconv.Itoa(index)+",\"name\":\""+text(4)+"\",\"active\":true,\"tags\":[\"one\",\"two\"]}")
		}
	}
	return documents
}

func transformJSON(documents []string) int64 {
	var checksum int64
	for _, document := range documents {
		var fields map[string]any
		if err := json.Unmarshal([]byte(document), &fields); err != nil {
			checksum++
			continue
		}
		id, ok := fields["id"].(float64)
		if !ok {
			checksum -= 1000000
			continue
		}
		output, err := json.Marshal([]any{int64(id) + 1, fields["name"], fields["active"]})
		if err != nil {
			checksum -= 1000000
			continue
		}
		checksum += size(string(output))
	}
	return checksum
}

type workerState struct {
	cache     []string
	completed int64
}

func processJobs(state *workerState, count, batch int) int64 {
	var checksum int64
	for index := 0; index < count; index++ {
		payload := "job-" + strconv.Itoa(batch) + "-" + strconv.Itoa(index) + "-" + text(8)
		if index%17 == 0 {
			checksum++
			continue
		}
		if index%11 == 0 {
			payload += "-retry"
		}
		state.cache[(index+batch)%len(state.cache)] = payload
		state.completed++
		checksum += size(payload)
	}
	for _, payload := range state.cache {
		checksum += size(payload)
	}
	return checksum + state.completed
}

func hashBatch(count int, variant string) int64 {
	values := make(map[string]int64)
	for index := 0; index < count; index++ {
		values["key-"+strconv.Itoa(index)] = int64(index)
	}
	var checksum int64
	for index := 0; index < count; index++ {
		selected := index
		if variant == "miss-heavy" && index%10 != 0 {
			selected += count
		}
		if value, ok := values["key-"+strconv.Itoa(selected)]; ok {
			checksum += value
		} else {
			checksum++
		}
	}
	return checksum
}

func stringBatch(count int, variant string) int64 {
	width := 4
	if variant == "long" {
		width = 512
	}
	line := text(width) + ",last"
	var checksum int64
	for index := 0; index < count; index++ {
		for _, part := range strings.Split(line, ",") {
			checksum += size(part)
			if strings.Contains(part, "😀") {
				checksum++
			}
		}
	}
	return checksum
}

func arrayBatch(count int, variant string) int64 {
	values := make([]int64, 0, count)
	for index := 0; index < count; index++ {
		value := int64((index*7919 + 17) % 100003)
		switch variant {
		case "sorted":
			value = int64(index)
		case "reverse":
			value = int64(count - index)
		case "duplicates":
			value = int64(index % 8)
		}
		values = append(values, value)
	}
	sorted := slices.Clone(values)
	slices.Sort(sorted)
	var checksum int64
	for index, value := range sorted {
		checksum = (checksum + value*int64(index%7+1)) % 1000000007
	}
	return checksum
}

func allocationBatch(retained []string, count int, variant string, batch int) int64 {
	var checksum int64
	for index := 0; index < count; index++ {
		value := "object-" + strconv.Itoa(batch) + "-" + strconv.Itoa(index) + "-" + text(16)
		checksum += size(value)
		if variant == "retained" {
			retained[index%len(retained)] = value
		}
	}
	return checksum
}

func main() {
	workload, variant := os.Args[1], os.Args[3]
	count, err := strconv.Atoi(os.Args[2])
	if err != nil {
		panic(err)
	}
	batches, err := strconv.Atoi(os.Args[4])
	if err != nil {
		panic(err)
	}
	var lines []string
	if workload == "log-pipeline" {
		lines = logInput(count, variant)
	}
	if workload == "json-transform" {
		lines = jsonInput(count, variant)
	}
	state := workerState{cache: make([]string, 128)}
	var retained []string
	if workload == "allocation" && variant == "retained" {
		retained = make([]string, count)
	}
	fmt.Println("ready")
	for batch := 0; batch < batches; batch++ {
		var checksum int64
		switch workload {
		case "log-pipeline":
			checksum = aggregateLogs(lines)
		case "json-transform":
			checksum = transformJSON(lines)
		case "worker":
			checksum = processJobs(&state, count, batch)
		case "hash":
			checksum = hashBatch(count, variant)
		case "strings":
			checksum = stringBatch(count, variant)
		case "arrays":
			checksum = arrayBatch(count, variant)
		case "allocation":
			checksum = allocationBatch(retained, count, variant, batch)
		default:
			panic("unknown workload")
		}
		fmt.Printf("%d,%d\n", batch, checksum)
	}
	var retainedSize int64
	for _, value := range retained {
		retainedSize += size(value)
	}
	fmt.Printf("done,%d\n", retainedSize)
}
