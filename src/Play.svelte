<script>
	import {Home,invHome,selected} from './lib/stores.js'
	import { Body } from 'svelte-body'
	import { fade,fly } from 'svelte/transition'
	import _ from 'lodash'
	import {log} from './lib/utils.js'

	let delay = 10 // s
	const DURATION = 1000 // ms
	const GAP = 30
	let i=0
	let paused = false
	let seconds = delay
	let directory = 'Home/' // eller 'small/'

	$: keys = _.filter(_.keys($selected), (key) => $selected[key])
	$: n = keys.length
	$: ih = $invHome[keys[i%n]]
	$: bw = ih.bw
	$: bh = ih.bh
	$: md5 = ih.md5
	$: path = ih.path + '/' + ih.filename
	const host = location.origin + location.pathname.replace('index.html','')
	$: log('origin',location.origin)
	$: log('pathname',location.pathname)
	$: href = host + directory + md5 + '.jpg'
	$: log(href.replace('https://storage.googleapis.com/',''))

	$: key = _.last(path.split('/')).replaceAll('_',' ').replace('.jpg','').replace('Vy-','')

	const f = () => {
		if (seconds==0) {
			i = paused ? i : i+1
			seconds = delay
		} else {
			seconds--
		}
		setTimeout(f,1000)
	}
	setTimeout(f,1000)

	$: skala  = Math.min((innerHeight-GAP)/bh, (innerWidth)/bw)
	$: width  = Math.round(bw * skala * 0.98)
	$: height = Math.round(bh * skala * 0.98)
	$: left   = Math.round((innerWidth - width)/2)
	$: top    = GAP

	function g(i1) {
		i = i1
		seconds = delay
	}

	function keydown(event) {
		const key = event.key
		if (key == ' ') paused = ! paused
		if (key == '1') directory = 'small/'
		if (key == '2') directory = 'Home/'
		if (key == 'ArrowLeft') g(i-1)
		if (key == 'ArrowRight') g(i+1)
		if (key == 'ArrowUp')   {
			delay++
			g(i)
		}
		if (key == 'ArrowDown') {
			delay = delay <= 5 ? delay : delay-1
			g(i)
		}
		if (key == 'Home') g(0)
		if (key == 'End') g(n-1)
	}

	window.onscroll = (e)=> {
		e.preventDefault()
		e.stopPropagation()
		return false
	}

</script>

<svelte:window on:keydown={keydown}/>

<Body style="background-color: black; color:white" />

<div>

	<table width=99%>
		<tr><td style='text-align:left' width=10%>
			#{i%n}
		</td><td style='text-align:center' width=80%>
			{paused ? 'Paused (Keys: Space 1=Lo 2=Hi Home Left Right Up Down End)' : key}
		</td><td style='text-align:right' width=10%>
			{seconds}s
		</td></tr>
	</table>

	{#key i}
		<img transition:fade = {{duration:DURATION}} style="position:absolute;left:{left}px;top:{top}px;" width={width}px  src={href} alt="">
	{/key}

</div>

<style>
	img {border-radius: 1%}
</style>
