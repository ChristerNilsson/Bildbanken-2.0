<script>
	import Card from './Card.svelte'
	export let WIDTH
	export let cards
</script>

{#each cards as card}
	<Card {WIDTH} {card} />
{/each}
