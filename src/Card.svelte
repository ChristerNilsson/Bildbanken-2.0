<script>
	import _ from "lodash"
	import {log,prettyFilename,round} from './lib/utils.js'
	import {fileIndex,invHome,images,selected} from './lib/stores.js'

	export let WIDTH
	export let card

	$: ih = $invHome[card.md5]
	$: filename = ih.path + "/" + ih.filename

	$: FS = getNumbers(filename,'F')
	$: LS = getNumbers(filename,'L')
	$: IS = getNumbers(filename,'I')
	$: RS = getNumbers(filename,'R')
	$: MS = getNumbers(filename,'M')
	$: TS = getNumbers(filename,'T')
	$: VS = getNumbers(filename,'V')

	function getNumbers(path,letter) { // Används för filnummer = MTV FLIR member tournament video file (deprecated) link invite result
		let matches
		if (letter=='F') matches = path.matchAll(/[F]\d+/g) // Facts
		if (letter=='L') matches = path.matchAll(/[L]\d+/g)
		if (letter=='I') matches = path.matchAll(/[I]\d+/g)
		if (letter=='R') matches = path.matchAll(/[R]\d+/g)
		if (letter=='M') matches = path.matchAll(/[M]\d+/g)
		if (letter=='T') matches = path.matchAll(/[T]\d+/g)
		if (letter=='V') matches = path.matchAll(/[V]\d+/g)
		if (! matches) return []
		matches = [...matches]
		return _.map(matches, (match) => match[0].slice(1)) // skippa bokstaven
	}

	function prettyPath(path) { // Tag bort eventuellt T-nummer
		path = path.split('/')
		path = path.slice(2,path.length-1)
		path = path.join(" • ")
		path = path.replaceAll(/_F\d+/g,'') // Facts
		path = path.replaceAll(/_L\d+/g,'')
		path = path.replaceAll(/_I\d+/g,'')
		path = path.replaceAll(/_R\d+/g,'')
		path = path.replaceAll(/_M\d+/g,'')
		path = path.replaceAll(/[ _]T\d\d\d\d\d/g,'')
		path = path.replaceAll(/_V\d+/g,'')
		return path.replaceAll('_', ' ')
	}

	function flip() {
		$selected[card.md5] = ! $selected[card.md5]
	}
	function noop(){}

</script>

<div class="card" id="images" style="position:absolute; width:{WIDTH}px; left:{card.x}px; top:{card.y}px">
	<img
		margin:0px
		padding:0px
		src = {"small/" + card.md5 + ".jpg"}
		width = {WIDTH}px
		alt = ""
		on:click = {() => {
			const host = location.origin + location.pathname
			const ih = $invHome[card.md5]
			// state = 'PICTURE'
			// visaBig(card.md5)
			window.open(host + `?md5=${card.md5}`)
		}}
		on:keydown = {() =>{}}
	/>
	<div class="group">
		<div class="info" style="width:{WIDTH}px" on:click = {flip} on:keyup={noop}>
			&nbsp;{prettyFilename(filename)}
		</div>
		<div class="info" style="width:{WIDTH}px" on:click = {flip} on:keyup={noop}>
			&nbsp;{prettyPath(filename)}
		</div>
		<div class="info" style="display:flex; height:13px; width:{WIDTH}px" on:click = {flip} on:keyup={noop}>
			&nbsp;{card.index}

			{#if card.letters}
				&nbsp;{card.letters}
			{/if}

			&nbsp;<input class="largerCheckbox" type="checkbox" bind:checked={$selected[card.md5]} />
			&nbsp;© Lars OA
			{#each FS as F}&nbsp;<a target="_blank" href="{$fileIndex[F]}">Facts</a>{/each}
			{#each LS as L}&nbsp;<a target="_blank" href="{$fileIndex[L]}">Link</a>{/each}
			{#each IS as I}&nbsp;<a target="_blank" href="{$fileIndex[I]}">Invite</a>{/each}
			{#each RS as R}&nbsp;<a target="_blank" href="{$fileIndex[R]}">Result</a>{/each}
			{#each MS as M}&nbsp;<a target="_blank" href="https://member.schack.se/ViewPlayerRatingDiagram?memberid={M}">Member</a>{/each}
			{#each TS as T}&nbsp;<a target="_blank" href="https://member.schack.se/ShowTournamentServlet?id={T}&listingtype=2">Result</a>{/each}
			{#each VS as V}&nbsp;<a target="_blank" href="https://player.vimeo.com/video/{V}">Video</a>{/each}
			<!-- <span style="flex:2; text-align:center; white-space:nowrap;"></span> -->
			<!-- • {round(ih.bw*ih.bh/1024/1024,1)}MP -->
			<span style="flex:1; text-align:right; white-space:nowrap;"> {ih.timestamp.slice(0,16)} • {ih.bw}x{ih.bh} • {round(ih.bs/1024,0)}kB</span>
		</div>	
	</div>
</div>

<style>
	input.largerCheckbox {
		width: 12px;
		height: 12px;
	}	
	.group {
		margin-top:-3px;
	}
	.info {
		margin:0px;
		text-align:left;
		padding-top:0px;
		white-space:nowrap;
		overflow:hidden;
		background-color:lightgray;
	}
	.card {
		/* margin:0px; */
		/* font-size: 12px; */
		/* max-height: 800px; */
	}
	div {
		margin: 0px;
		padding: 0px;
		font-size: 13px;
	}
</style>
