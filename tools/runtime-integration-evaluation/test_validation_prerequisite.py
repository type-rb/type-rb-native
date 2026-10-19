import copy
import hashlib
import unittest

import qualify


class MeasurementPrerequisiteTests(unittest.TestCase):
    def setUp(self):
        self.log = b"Failed to CreateArtifact: Unable to make request: ENOTFOUND\n"
        names = [f"Correctness step {index}" for index in range(21)]
        self.registration = dict(
            candidate="a" * 40, validationRevision="a" * 40,
            requiredValidationRun=1, requiredCompleteRun=1,
            requiredCompleteJobs=["quick", "native / verify", "Native CI acceptance"],
            measurementPrerequisite=dict(
                kind="successful-correctness-with-frozen-upload-dns-failure",
                runAttempt=1, nativeJob=2, acceptanceJob=3,
                nativeLogSHA256=hashlib.sha256(self.log).hexdigest(),
                requiredNativeSteps=names, adoptionRequiresStrictCI=True,
            ),
        )
        run = dict(id=1, head_sha="a" * 40, run_attempt=1, event="pull_request",
                   name="Pull request validation", status="completed", conclusion="failure")
        passed = lambda name: dict(name=name, status="completed", conclusion="success")
        native = dict(passed("native / verify"), id=2, conclusion="failure", steps=[
            *[passed(name) for name in names],
            dict(passed("Upload joined suite logs, ownership receipt and cleanup outcome"), conclusion="failure"),
        ])
        acceptance = dict(passed("Native CI acceptance"), id=3, conclusion="failure", steps=[
            dict(passed("Require all applicable authorities, not skipped-job success"), conclusion="failure"),
        ])
        self.evidence = dict(production=run, complete=run,
                             completeJobs=dict(jobs=[passed("quick"), native, acceptance]))

    def validate(self, evidence=None, registration=None, log=None):
        qualify.validate_measurement_ci(
            self.evidence if evidence is None else evidence,
            self.registration if registration is None else registration,
            self.log if log is None else log,
        )

    def test_transport_failure_allows_measurement_but_not_adoption(self):
        self.validate()
        with self.assertRaises(ValueError):
            qualify.validate_ci(self.evidence, self.registration)

    def test_every_native_correctness_step_must_pass(self):
        for index in range(21):
            for outcome in ("failure", "skipped", None):
                with self.subTest(index=index, outcome=outcome):
                    evidence = copy.deepcopy(self.evidence)
                    evidence["completeJobs"]["jobs"][1]["steps"][index]["conclusion"] = outcome
                    with self.assertRaises(ValueError):
                        self.validate(evidence=evidence)

    def test_other_failed_missing_duplicate_or_skipped_jobs_block_measurement(self):
        for outcome in ("failure", "skipped", None):
            evidence = copy.deepcopy(self.evidence)
            evidence["completeJobs"]["jobs"][0]["conclusion"] = outcome
            with self.assertRaises(ValueError):
                self.validate(evidence=evidence)
        for replacement in (self.evidence["completeJobs"]["jobs"][1:],
                            self.evidence["completeJobs"]["jobs"] * 2):
            evidence = copy.deepcopy(self.evidence)
            evidence["completeJobs"]["jobs"] = replacement
            with self.assertRaises(ValueError):
                self.validate(evidence=evidence)

    def test_wrong_attempt_source_job_or_log_is_rejected(self):
        for field, value in (("run_attempt", 2), ("head_sha", "b" * 40),
                             ("status", "in_progress"), ("conclusion", "success")):
            evidence = copy.deepcopy(self.evidence)
            evidence["complete"][field] = value
            with self.assertRaises(ValueError):
                self.validate(evidence=evidence)
        for position in (1, 2):
            evidence = copy.deepcopy(self.evidence)
            evidence["completeJobs"]["jobs"][position]["id"] = 99
            with self.assertRaises(ValueError):
                self.validate(evidence=evidence)
        with self.assertRaises(ValueError):
            self.validate(log=self.log + b"changed")

    def test_missing_inventory_or_removed_adoption_gate_is_rejected(self):
        for field, value in (("requiredNativeSteps", []), ("adoptionRequiresStrictCI", False)):
            registration = copy.deepcopy(self.registration)
            registration["measurementPrerequisite"][field] = value
            with self.assertRaises(ValueError):
                self.validate(registration=registration)


if __name__ == "__main__":
    unittest.main()
