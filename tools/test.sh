# https://ghcr.io/tomp736/pymp/pymp_core/tags
registry_server="ghcr.io"
user="tomp736"
image="pymp/pymp_core"
image_encoded="pymp%2Fpymp_core"

TAGS=$(curl -L \
    -H "Accept: application/vnd.github+json" \
    -H "Authorization: Bearer $token" \
    https://api.github.com/users/$user/packages/container/$image_encoded/versions \
    | jq -r '.[] | [.url, .metadata.container.tags[] // "" ] | @csv')

echo "$TAGS" | while IFS=',' read -r package_url package_tag; do

    echo "Checking $package_url : $package_tag"

    if [[ "$package_tag" =~ ^[0-9]+\.[0-9]+\.[09]+$ ]]; then
        echo "Tag valid: $user/$image:$package_tag"
    elif [[ "$package_tag" = 'latest' ]]; then
        echo "Tag valid: $user/$image:$package_tag"
    else
        echo "Tag invalid: $user/$image:$package_tag"
        url=$(echo $package_url | tr -d '"')
        echo $url
        curl \
            -X DELETE \
            -H "Accept: application/vnd.github+json" \
            -H "Authorization: Bearer $token" \
            $url
    fi

done