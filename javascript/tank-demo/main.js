var Map = function() {
	this.x = 0;
	this.y = 0;
	
	this.objects = [];

	this.addObject = function(object) {
		this.objects.push(object);
	};

	this.render = function() {
		$("body").attr("style",
			"background-position-x:" + this.x + 
			"px;background-position-y:" + this.y + "px");

		for (index in this.objects) {
			this.objects[index].render();
		}
	};

	this.move = function(dx, dy) {
		this.x -= dx * 0.6;
		this.y -= dy * 0.6;
	};

	this.onKeyDown = function(ev){
		for (index in this.objects) {
			this.objects[index].onKeyDown(ev);
		}
		this.render();
	};
};

var Tank = function(map, x, y) {
	this.map = map;
	this.x = x;
	this.y = y;

	this.vec = "north";

	this .SELECTOR = "#tank";

	this.sprites = {
		"south" : "s.png",
		"east" : "e.png",
		"west" : "w.png",
		"north" : "n.png"
	};
	
	var tank = this;

	this.actions = {
		"go_west": function() {
				tank.movingAction(-5, 0, "west");
			},
		"go_north": function() {
				tank.movingAction(0, -5, "north");
			},
		"go_east": function() {
				tank.movingAction(5, 0, "east");
			},
		"go_south": function() {
				tank.movingAction(0, 5, "south");
			},
	};

	
	this.keyMap = {
		37: "go_west",
		38: "go_north",
		39: "go_east",
		40: "go_south",

		65: "go_west",
		87: "go_north",
		68: "go_east",
		83: "go_south",
	};

	this.render = function() {
		$(this .SELECTOR).attr("src", "./imgs/" + this.sprites[this.vec]);
		$(this .SELECTOR).attr("style", "top:" + this.y + "; left:" + this.x);
	};

	this.movingAction = function(dx, dy, vec) {
		var docWidth = $("body").width();
		var docHeight = $("body").height();
	
		var BOUNDARY = 50;

		this.vec = vec;
	
		if (dx != 0) {
			if (dx < 0) {
				if (this.x > BOUNDARY) {
					this.x += dx;
				} else {
					this.map.move(dx, 0);
				}
			} else {
				if (this.x < docWidth - BOUNDARY - $(this .SELECTOR).width()) {
					this.x += dx;
				} else {
					this.map.move(dx, 0);
				}
			}
		}
	
		if (dy != 0) {
			if (dy < 0) {
				if (this.y > BOUNDARY) {
					this.y += dy;
				} else {
					this.map.move(0, dy);
				}
			} else {
				if (this.y < docHeight - BOUNDARY - $(this .SELECTOR).height()) {
					this.y += dy;
				} else {
					this.map.move(0, dy);
				}
			}
		}
	};

	this.onKeyDown = function(ev){
		action = this.keyMap[ev.keyCode];
		if (action) {
			this.actions[action]();
		}
	};
};

var map  = new Map();
var tank = new Tank(map, 100, 100);
map.addObject(tank);

$(document).ready(function(){
	tank.render();
	
	$(document).keydown(function(ev) {
		map.onKeyDown(ev);
	});
});
