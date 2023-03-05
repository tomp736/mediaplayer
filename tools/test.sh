# https://ghcr.io/tomp736/pymp/pymp_core/tags
registry_server="ghcr.io"
user="tomp736"
image="pymp/pymp_core"
image_encoded="pymp%2Fpymp_core"

CONTAINERS=$(curl -L \
    -H "Accept: application/vnd.github+json" \
    -H "Authorization: Bearer $read_token" \
    https://api.github.com/users/$user/packages/container/$image_encoded/versions \
    jq -r '.[] | [.name, .metadata.container.tags[] // "" ] | @csv')
    

echo "$CONTAINERS" | while IFS=',' read -r container_name container_tag; do
    if [[ "$container_tag" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
        echo "Tag valid: $user/$image:$tag"
    elif [[ "$container_tag" = 'latest' ]]; then
        echo "Tag valid: $user/$image:$tag"
    else
        echo "Tag invalid: $user/$image:$tag"

        curl -L \
            -X DELETE \
            -H "Accept: application/vnd.github+json" \
            -H "Authorization: Bearer $write_token" \
            https://api.github.com/users/$user/packages/container/$image_encoded/versions/$container_name
    fi
done
