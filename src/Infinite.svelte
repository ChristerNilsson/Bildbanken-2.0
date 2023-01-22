<script>
	import Card from './Card.svelte'
	export let WIDTH
	export let cards
	export let round
	export let fileWrapper
	export let prettyFilename
</script>

{#each cards as card}
	<Card {WIDTH} {card} {round} {fileWrapper} {prettyFilename} />
{/each}
