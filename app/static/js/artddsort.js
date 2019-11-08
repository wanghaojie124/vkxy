;(function( $ ){
	$.fn.DDSort = function( options ){
		var $doc = $( document ),
			fnEmpty = function(){},

			settings = $.extend( true, {

				down: fnEmpty,
				move: fnEmpty,
				up: fnEmpty,

				target: 'li',
				cloneStyle: {
					'background-color': '#eee'
				},
				floatStyle: {
					//用固定定位可以防止定位父级不是Body的情况的兼容处理，表示不兼容IE6，无妨
					'position': 'fixed',
					'box-shadow': '10px 10px 20px 0 #eee',
					// 'webkitTransform': 'rotate(4deg)',
					// 'mozTransform': 'rotate(4deg)',
					// 'msTransform': 'rotate(4deg)',
					// 'transform': 'rotate(4deg)'
				}

			}, options );

		return this.each(function(){

			var that = $( this ),
				height = 'height',
				width = 'width';

			if( that.css( 'box-sizing' ) == 'border-box' ){
				height = 'outerHeight';
				width = 'outerWidth';
			}

			that.on( 'mousedown.DDSort', settings.target, function( e ){
				//只允许鼠标左键拖动
				if( e.which != 1 ){
					return;
				}
				
				//防止表单元素失效
				var tagName = e.target.tagName.toLowerCase();
				if( tagName == 'input' || tagName == 'textarea' || tagName == 'select' ){
					return;
				}
				
				var THIS = this,
					$this = $( THIS ),
					offset = $this.offset(),
					disX = e.pageX - offset.left,
					disY = e.pageY - offset.top,
				
					clone = $this.clone()
						.css( settings.cloneStyle )
						.css( 'height', $this[ height ]() )
						.empty(),
						
					hasClone = 1,

					//缓存计算
					thisOuterHeight = $this.outerHeight(),
					thatOuterHeight = that.outerHeight(),

					//滚动速度
					upSpeed = thisOuterHeight,
					downSpeed = thisOuterHeight,
					maxSpeed = thisOuterHeight * 3;
				
				settings.down.call( THIS );
				
				$doc.on( 'mousemove.DDSort', function( e ){
					if( hasClone ){
						$this.before( clone )
							.css( 'width', $this[ width ]() )
							.css( settings.floatStyle )
							.appendTo( $this.parent() );
							
						hasClone = 0;
					}
					
					var left = e.pageX - disX,
						top = e.pageY - disY,
						
						prev = clone.prev(),
						next = clone.next().not( $this );
					
					$this.css({
						left: left,
						top: top
					});
					
					//向上排序
					if( prev.length && top < prev.offset().top + prev.outerHeight()/2 ){
							
						clone.after( prev );
						
					//向下排序
					}else if( next.length && top + thisOuterHeight > next.offset().top + next.outerHeight()/2 ){
						
						clone.before( next );

					}

					/**
					 * 处理滚动条
					 * that是带着滚动条的元素，这里默认以为that元素是这样的元素（正常情况就是这样），如果使用者事件委托的元素不是这样的元素，那么需要提供接口出来
					 */
					var thatScrollTop = that.scrollTop(),
						thatOffsetTop = that.offset().top,
						scrollVal;
					
					//向上滚动
					if( top < thatOffsetTop ){

						downSpeed = thisOuterHeight;
						upSpeed = ++upSpeed > maxSpeed ? maxSpeed : upSpeed;
						scrollVal = thatScrollTop - upSpeed;

					//向下滚动
					}else if( top + thisOuterHeight - thatOffsetTop > thatOuterHeight ){

						upSpeed = thisOuterHeight;
						downSpeed = ++downSpeed > maxSpeed ? maxSpeed : downSpeed;
						scrollVal = thatScrollTop + downSpeed;
					}

					that.scrollTop( scrollVal );

					settings.move.call( THIS );
					// alert(88888)
				})
				.on( 'mouseup.DDSort', function(){
					
					$doc.off( 'mousemove.DDSort mouseup.DDSort' );
					
					//click的时候也会触发mouseup事件，加上判断阻止这种情况
					if( !hasClone ){
						clone.before( $this.removeAttr( 'style' ) ).remove();
						settings.up.call( THIS );
						 var Arrayindex =[];
					 	var Arrayforitem = [];
					 	 $(".mynode").each(function(){
		                 // alert($(this).parent().siblings('.nodeindex').html())
		                // alert($(this).parent().siblings('.nodeindex').html())
		                // 重新排序了，并更新数据，考虑分页的情况
		                var arrindex=$('.mynode').wx_mini(this);
		                var foritem=$(this).attr('id');
		                var newindex=$('.mynode').wx_mini(this)*1+1;
		                $(this).parent().siblings('.nodeindex').html(newindex)
		                // 更新数据，每个foritem对应一个新的顺序
		                // Arrayindex[arrindex]=newindex;
		                Arrayindex.push(newindex)
		                Arrayforitem.push(foritem)
		                console.log(Arrayindex)
		                console.log(Arrayforitem)
		                // Arrayforitem[arrindex]=foritem;
		               Aindex = Arrayindex.join(",");
		               Aforitem=Arrayforitem.join(",");
		            });
					  $.post("/admin/artrankUpdate.php",
				              {
				                Arrayindex:Aindex,
				                foritem:Aforitem
				              },
				              function(data,status){
				              	// console.log(Arrayforitem[0])
				               // alert("Data: " + data['status'] + "nStatus: " + status);
				               console.log(data)
				              });	 
					}
				});
			
				return false;

			});

		});
		 
          

       
	};

})( jQuery );