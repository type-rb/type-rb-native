#!/bin/sh

set -eu

fail() {
	printf 'benchmarksgame-cpuset-delegation: %s\n' "$1" >&2
	exit 1
}

test "$#" -eq 1 || fail "one evidence path is required"
evidence=$1
test "$(uname -s)" = Linux || fail "Linux is required"
test -x /usr/bin/id || fail "/usr/bin/id is required"
test -x /usr/bin/sudo || fail "/usr/bin/sudo is required"
test -x /usr/bin/tee || fail "/usr/bin/tee is required"
test -d "$(dirname -- "$evidence")" || fail "evidence parent does not exist"
test ! -e "$evidence" || fail "evidence path already exists"
test ! -e "$evidence.sudo.stdout" || fail "sudo stdout evidence already exists"
test ! -e "$evidence.sudo.stderr" || fail "sudo stderr evidence already exists"

user_id=$(/usr/bin/id -u)
case "$user_id" in
'' | *[!0-9]*) fail "current user ID is not numeric" ;;
esac

user_service=/sys/fs/cgroup/user.slice/user-$user_id.slice/user@$user_id.service
controllers=$user_service/cgroup.controllers
subtree_control=$user_service/cgroup.subtree_control
test -r "$controllers" || fail "systemd user-service cgroup controllers are unavailable"
test -r "$subtree_control" || fail "systemd user-service subtree control is unavailable"
grep -qw cpuset "$controllers" || fail "cpuset is not available to the systemd user service"

{
	printf 'user_id=%s\n' "$user_id"
	printf 'user_service=%s\n' "$user_service"
	printf 'current_cgroup=%s\n' "$(awk -F: '$1 == 0 { print $3 }' /proc/self/cgroup)"
	printf 'available_controllers=%s\n' "$(cat "$controllers")"
	printf 'subtree_control_before=%s\n' "$(cat "$subtree_control")"
} > "$evidence"

: > "$evidence.sudo.stdout"
: > "$evidence.sudo.stderr"
if ! grep -qw cpuset "$subtree_control"; then
	set +e
	printf '+cpuset\n' |
		/usr/bin/sudo -n /usr/bin/tee "$subtree_control" > "$evidence.sudo.stdout" 2> "$evidence.sudo.stderr"
	delegation_status=$?
	set -e
	test "$delegation_status" -eq 0 || fail "could not delegate cpuset"
fi

printf 'subtree_control_after=%s\n' "$(cat "$subtree_control")" >> "$evidence"
grep -qw cpuset "$subtree_control" || fail "cpuset remains unavailable after delegation"
printf 'benchmarksgame-cpuset-delegation: cpuset is delegated\n'
