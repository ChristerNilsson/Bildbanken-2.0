<script>
	// import _ from "lodash"
	import {is_jpg} from './lib/utils.js'
	import {Home} from './lib/stores.js'

	let lines = []
	function recurse (node,path="") {
		lines.push(path)
		for (const key in node) {
			if (!is_jpg(key)) recurse(node[key], path==''? key : path + ' • ' + key)
		}
	}
	recurse($Home)

</script>

{#each lines as line}
	&nbsp;&nbsp;{line}<br>
{/each}
