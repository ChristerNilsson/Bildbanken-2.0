<script>
	// import _ from "lodash"
	import {is_jpg} from './lib/utils.js'
	import {Home} from './lib/stores.js'

	let lines = []
	function recurse (node,key0,level=0) {
		lines.push(' • '.repeat(level)+key0)
		for (const key in node) {
			if (!is_jpg(key)) recurse(node[key], key,level+1)
		}
	}
	recurse($Home,'Home')

</script>

{#each lines as line}
	&nbsp;&nbsp;{line}<br>
{/each}
