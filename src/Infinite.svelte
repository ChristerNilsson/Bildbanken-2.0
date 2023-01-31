<script>
	import Card from './Card.svelte'
	export let WIDTH
	export let cards
	export let prettyFilename
</script>

{#each cards as card}
	<Card {WIDTH} {card} {prettyFilename} />
{/each}
