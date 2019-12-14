import React, { useState, useEffect } from 'react';
import connect from '@vkontakte/vk-connect';
import View from '@vkontakte/vkui/dist/components/View/View';
import ScreenSpinner from '@vkontakte/vkui/dist/components/ScreenSpinner/ScreenSpinner';
import '@vkontakte/vkui/dist/vkui.css';
import {Panel, PanelHeader, Group, List, Cell, Button } from '@vkontakte/vkui';


import Home from './panels/Home';
//import Persik from './panels/Persik';


const onStop = (blob) => {
	// Do something with the blob file of the recording
  }

function App () {
	return (
		
	  <View activePanel="main">
		  
		<Panel id="main">
		  <PanelHeader>VKUI</PanelHeader>
		  <Group title="buttons">
			<div>
			<Button id='rec'>start</Button>
			
				<Button id='stop'>stop</Button>

				<Button id='play_pause'>play</Button>

				<Button id='rew'>download</Button>

				<Button id='ff'>but4</Button>
			</div>
			<script type="text/javascript">
		

		
</script>
			
		  </Group>
		</Panel>
	  </View>
	  
	);
  }
	


 

export default App;

