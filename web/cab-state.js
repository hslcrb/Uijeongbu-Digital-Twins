// Fictional game controls, not operational railway instructions.
export class CabState {
 constructor({distance=0,length=1000,station=distance}){this.d=distance;this.length=length;this.station=station;this.v=0;this.power=0;this.doors=false;this.direction=1;this.mode='outside';}
 enter(){if(Math.abs(this.v)>.05||!this.doors)return false;this.mode='vestibule';return true;}
 cab(){if(this.mode!=='vestibule')return false;this.mode='cab';return true;}
 toggleDoors(){if(Math.abs(this.v)>.05||Math.abs(this.d-this.station)>3)return false;this.doors=!this.doors;if(this.doors)this.power=0;return true;}
 command(value){if(this.mode!=='cab'||this.doors)return false;this.power=Math.max(-1,Math.min(1,value));return true;}
 reverse(){if(Math.abs(this.v)>.05)return false;this.direction*=-1;return true;}
 exit(){if(Math.abs(this.v)>.05||!this.doors)return false;this.mode='outside';return true;}
 update(dt){dt=Math.max(0,Math.min(.1,dt));if(this.doors){this.v=0;return;}this.v=Math.max(0,Math.min(24,this.v+(this.power>0?1.2*this.power:this.power<0?2.8*this.power:-.2)*dt));this.d=Math.max(0,Math.min(this.length,this.d+this.v*this.direction*dt));if(this.d===0||this.d===this.length){this.v=0;this.power=0;}}
}
