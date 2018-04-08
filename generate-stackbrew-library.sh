#!/usr/bin/env bash
set -Eeuo pipefail

declare -A aliases=(
	[1.25.0]='1 1.25 latest'
)

defaultDebianSuite='stretch'
declare -A debianSuites=(
)

self="$(basename "$BASH_SOURCE")"
cd "$(dirname "$(readlink -f "$BASH_SOURCE")")"

source '.metadata-lib'

versions=( */ )
versions=( "${versions[@]%/}" )

# sort version numbers with highest first
IFS=$'\n'; versions=( $(echo "${versions[*]}" | sort -rV) ); unset IFS

# get the most recent commit which modified any of "$@"
fileCommit() {
	git log -1 --format='format:%H' HEAD -- "$@"
}

# get the most recent commit which modified "$1/Dockerfile" or any file COPY'd from "$1/Dockerfile"
dirCommit() {
	local dir="$1"; shift
	(
		cd "$dir"
		fileCommit \
			Dockerfile \
			$(git show HEAD:./Dockerfile | awk '
				toupper($1) == "COPY" {
					for (i = 2; i < NF; i++) {
						print $i
					}
				}
			')
	)
}

cat <<-EOH
# this file is generated via https://github.com/rust-lang-nursery/docker-rust/blob/$(fileCommit "$self")/$self

Maintainers: Steven Fackler <sfackler@gmail.com> (@sfackler)
GitRepo: https://github.com/rust-lang-nursery/docker-rust.git
EOH

# prints "$2$1$3$1...$N"
join() {
	local sep="$1"; shift
	local out; printf -v out "${sep//%/%%}%s" "$@"
	echo "${out#$sep}"
}

for version in "${versions[@]}"; do
	debianSuite="${debianSuites[$version]:-$defaultDebianSuite}"

	for v in \
			{stretch,jessie}{,/slim} \
	; do
		dir="$version/$v"
		variant="$(basename "$v")"

		if [ "$variant" = 'slim' ]; then
			# convert "slim" into "slim-jessie"
			# https://github.com/docker-library/ruby/pull/142#issuecomment-320012893
			variant="$variant-$(basename "$(dirname "$v")")"
		fi

		[ -f "$dir/Dockerfile" ] || continue

		commit="$(dirCommit "$dir")"

		versionAliases=(
			$version
			${aliases[$version]:-}
		)

		variantAliases=( "${versionAliases[@]/%/-$variant}" )
		case "$variant" in
			*-"$debianSuite") # "slim-stretch", etc need slim
				variantAliases+=( "${versionAliases[@]/%/-${variant%-$debianSuite}}" )
				;;
		esac
		variantAliases=( "${variantAliases[@]//latest-/}" )

		versionSuite="${debianSuites[$version]:-$defaultDebianSuite}"

		case "$v" in
			*)  variantArches="$(variantArches "$version" "$v")" ;;
		esac

		if [ "$variant" = "$debianSuite" ]; then
			variantAliases+=( "${versionAliases[@]}" )
		fi

		echo
		cat <<-EOE
			Tags: $(join ', ' "${variantAliases[@]}")
			Architectures: $(join ', ' $variantArches)
			GitCommit: $commit
			Directory: $dir
		EOE
	done
done
