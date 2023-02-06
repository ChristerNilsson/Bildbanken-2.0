<script>
	import _ from "lodash"
	import {is_jpg,log} from './lib/utils.js'
	// import {rowsVertical} from './lib/stores.js'

	export let buttons
	export let visibleKeys
	export let push
	export let WIDTH
	export let spaceShip
	export let stack
	// export let rowsVertical

	buttons = false

	// $: $rowsVertical = (buttons ? 1 : 0)
	
	function sortera(keys,i) {
		// log({keys,i})
		const path = stack.join("/")
		buttons = (n == 2 && path != "Home/0000 Klubbar") 
		sortIndex = buttons ? i : 0

		let pos = sortIndex==1 ? 11 : 0
		keys.sort((a,b) => spaceShip(a.slice(pos),b.slice(pos)))
		if (n==1) keys.reverse()
		if (n==2 && buttons && sortIndex==0) keys.reverse()
		return keys
	}

	$: n = stack.length
	let sortIndex = 0
	$: keys = sortera(_.keys(visibleKeys),sortIndex)
	
	function clean(s) {
		s = s.replaceAll(/_M\d+/g,'')
		s = s.replaceAll(/[ _]T\d\d\d\d\d/g,'')
		s = s.replaceAll(/_V\d+/g,'')
		s = s.replaceAll(/_F\d+/g,'') // deprecated
		s = s.replaceAll(/_L\d+/g,'')
		s = s.replaceAll(/_I\d+/g,'')
		s = s.replaceAll(/_R\d+/g,'')
		s = s.replaceAll("_"," ")
		return s
	}
	
</script>

<div style="width:{WIDTH}px">

	{#if buttons}
		<div style="width:{WIDTH}px">
			<button class="header" style="left:0px; width:{90}px" on:click = {()=>keys=sortera(keys,0)}>Date</button>
			<button class="header" style="left:{90}px; width:{WIDTH-90-8}px" on:click = {()=>keys=sortera(keys,1)}>Event</button>
		</div>
	{:else}
		<div style="width:{WIDTH}px">
			<button class="header" style="left:0px; width:{WIDTH-2}px" on:click = {()=>keys=sortera(keys,0)}>Folders</button>
		</div>
	{/if}

	{#each keys as key }
		<div>
			<span>
				{#if ! is_jpg(key)}
					<button title="{clean(key)} ({visibleKeys[key]})" class="row" value={key} on:click = {() => push(key)}>
						{clean(key)} ({visibleKeys[key]})
					</button>
				{/if}
			</span>
		</div>
	{/each}
</div>

<style>
	span {
		flex:1;
		overflow:hidden;
		white-space:nowrap;
	}
	div {
		margin:0px
	}
	.header {
		margin:0.5px;
		height:30px;
	}
	.row {
		margin:2px;
		height:30px;
		width:99.5%;
		text-align:left;
		flex:1;
		overflow:hidden;
		white-space:nowrap;
	}

</style>
