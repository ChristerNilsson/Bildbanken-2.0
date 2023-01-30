<script>
	import Card from './Card.svelte'
	export let WIDTH
	export let cards
	// export let round
	// export let fileWrapper
	export let prettyFilename
	// export let state
	// export let visaBig
</script>

{#each cards as card}
	<Card {WIDTH} {card} {prettyFilename} />
{/each}
