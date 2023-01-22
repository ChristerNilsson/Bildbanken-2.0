<script>
	import Card from './Card.svelte'
	export let WIDTH
	export let cards
	export let round
	export let state
	export let fileWrapper
	export let prettyFilename
	export let visaBig
</script>

{#each cards as card}
	<Card bind:state {WIDTH} {card} {round} {fileWrapper} {prettyFilename} {visaBig}/>
{/each}
