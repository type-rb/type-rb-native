# Evidence retention

Retain the evidence needed to reproduce an acceptance or rejection, not every
generated file in the source checkout. This storage policy changes neither
measurement bounds nor which observations are retained. Failed observations,
warmups, outliers and rejected candidates must not disappear through cleanup.

## Source repository

Keep a dated result README with the conclusion, exact revisions, commands,
environment, measurement contract, all observation values and statuses in
compact CSV/TSV, derived summaries, source/artifact digests and archive location.
Preserve files consumed by compatibility checks, frozen-baseline policies and
Pages. Avoid duplicating drivers and source snapshots: link to exact revisions
or put a necessary reproduction in the maintained test/tool owner.

New result directories have a ceiling of **100 files and 2 MiB**, with no
individual new or changed file over **256 KiB**. Consolidate per-process tiny
files into tables. Do not add empty files, stdout/stderr sidecars, generated
executables, object files, QBE/assembly or compressed payloads to Git. Small
human-readable diagnostic logs remain useful within these limits. A necessary
exception requires an explicit policy review, not a silent limit increase.

`tools/result_archive.py check BASE HEAD` checks committed trees. Historical
unchanged files are grandfathered; an oversized result may shrink but cannot
grow beyond its previous size/count (or the normal ceiling). New/changed files
must meet the per-file policy. CI runs this with the actual PR/push base, not a
moving hand-picked measurement baseline. No performance rerun is needed for
storage-only changes; CI-routing changes still require their existing checks.

## Detailed public archives

Use a dedicated **evidence-only prerelease**, not a compiler/product release,
with a public `.tar.gz` asset. Do not update an existing asset in place. Record
its URL, SHA-256, size and source revision in each result's `ARCHIVE.json`.
The archive contains the original report, all files (including empty logs and
failed observations), and an internal per-file SHA-256/size/mode manifest.
Keep its source-era inventory; do not relabel it as a new measurement.

GitHub Actions artifacts are a temporary transport, not the only long-term
copy: they expire according to the configured retention period. Public release
assets also require stewardship; the digest detects replacement, it does not
guarantee permanent hosting. Preserve a backup before deleting or moving an
archive. See [GitHub artifact retention](https://docs.github.com/en/organizations/managing-organization-settings/configuring-the-retention-period-for-github-actions-artifacts-and-logs-in-your-organization).

For future measurements, publish the producing workflow's detailed evidence
before staging the compact result for Git. Do not temporarily commit raw files
on a PR branch and delete them in a later commit: that still grows Git history.
The `pack` command below is for migrating already-committed historical evidence,
not a requirement to commit new raw payloads first.

## Verified migration

1. Select exact committed public result directories; inspect external and
   cross-result consumers. Do not mix untracked files or private evidence.
2. Run `python3 tools/result_archive.py pack OUTPUT.tar.gz RESULT_ID ...` with
   an output outside the checkout. The deterministic archive includes only
   files whose bytes match the recorded Git revision; symlinks are rejected.
3. Upload the archive as a new evidence asset. Download it again from its public
   URL to a separate location and run `verify DOWNLOADED.tar.gz SHA256`.
   Confirm the download checksum and every member before removing any file.
4. Run `compact DOWNLOADED.tar.gz SHA256 PUBLIC_URL`. This stages only exact
   archived files for removal, preserves CSV/TSV/JSON/Markdown/checksum indexes,
   and adds an archive pointer and a storage notice. It rejects missing,
   changed or additional committed evidence. The command verifies local bytes;
   the operator must use the fresh public download from step 3, not assume
   that a successful upload proves availability.
5. Inspect the full diff and all remaining links. Run archive tests, the
   retention checker and Pages/compatibility consumers. Merge through a PR.

To inspect old detailed evidence, download the linked asset, verify its SHA-256
and manifest with `verify`, then extract it into a **new empty temporary
directory**, never over the working checkout. It restores the original
`results/RESULT_ID/` layout for source-era verifiers and checksum inventories.
The checked-in README's added storage notice is intentionally outside the
historical manifest; its original bytes are inside the archive.

Ordinary cleanup does not erase Git history. Existing history remains intact;
this work reduces current checkout size/file count and stops future raw-payload
growth. History rewriting and force pushes are not part of this policy.
