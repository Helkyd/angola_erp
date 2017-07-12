frappe.provide('angola_erp')


frappe.pages['jobcard'].on_page_load = function(wrapper) {
//frappe.ui.form.on("jobcard", "onload", function(frm,doctype,name) {

	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Job Card',
		single_column: true
	});

	var columns = [{ id: 'col0', name: 'Name, Vorname', toolTip: 'Name, Vorname der Person', sort_type: 'string' },
                   { id: 'col1', name: 'Gehalt',        toolTip: 'Gehalt der Person',        sort_type: 'float',     style: 'text-align: right;'},
                   { id: 'col2', name: 'Alter',         toolTip: 'Alter der Person',         sort_type: 'float',     style: 'text-align: right;', plot_master: true},
                   { id: 'col3', name: 'Geboren',       toolTip: 'Geburtsdatum der Person',  sort_type: 'date' },
    ];

    var options = { caption:            'Limited height and full width',
                    width:              '100%',
                    maxHeight:          100,
                    locale:              'en',
    };

    var data = [{ col0: 'Meier, Franz', col1: '4500,20', col2: '45', col3: '10.01.1962',
                },
                { col0: 'Huber, Xaver', col1: '2500,18', col2: '55', col3: '19.02.1958',
                  metadata: { columns: { col0: {title: 'Huber'}, col2: {title: 'Alter = 55', style: 'background-color: red;'}
                                       },
                            },
                },
                { col0: 'Beckenbauer, Heinrich', col1: '2500,18', col2: '61', col3: '14.11.1952',
                  metadata: { columns: { col0: {title: 'Beckenbauer'}, col2: {title: 'Alter = 61'}
                                       },
                            },
                },
                { col0: 'Schmidt, Walter', col1: '2500,18', col2: '61', col3: '14.11.1952',
                },
                { col0: 'Liebherr, Ulrich', col1: '2500,18', col2: '61', col3: '14.11.1952',
                  metadata: { columns: { col0: {title: 'Beckenbauer'}, col2: {title: 'Alter = 61'}
                                       },
                            },
                },
                { col0: 'Heinze, Karsten', col1: '2500,18', col2: '61', col3: '14.11.1952',
                  metadata: { columns: { col0: {title: 'Beckenbauer'}, col2: {title: 'Alter = 61'}
                                       },
                            },
                },
                { col0: 'Meutzner, Louis', col1: '2500,18', col2: '61', col3: '14.11.1952',
                  metadata: { columns: { col0: {title: 'Beckenbauer'}, col2: {title: 'Alter = 61'}
                                       },
                            },
                },
                { col0: 'Lexow, Lars', col1: '2500,18', col2: '61', col3: '14.11.1952',
                  metadata: { columns: { col0: {title: 'Beckenbauer'}, col2: {title: 'Alter = 61'}
                                       },
                            },
                },
    ];

   $("<table width='100%>\
		<tr>\
			<td valign='top' width='50%'>\
				<div id='demo_div' style='width:100%;height:500px;''></div>\
			</td>\
		</tr>\
	</table>").appendTo($(wrapper).find('.layout-main-section'));

    var additional_menu_entries = [{ label: 'Additional entry', hint: 'Additional entry just for fun', action: function(t){alert('Just for fun');} }];

    createSlickGridExtended('demo_div', data, columns, options, additional_menu_entries);

	$("<table width='100%>\
		<tr>\
			<td valign='top' width='50%'>\
				<div id='demo_div1' style='width:100%;height:500px;''></div>\
			</td>\
		</tr>\
	</table>").appendTo($(wrapper).find('.layout-main-section'));
	var campos;
	var dados;
	from_date = frappe.datetime.add_months(frappe.datetime.get_today(),-1)
	to_date = frappe.datetime.get_today()

	frappe.call({
		method:"angola_erp.angola_erpnext.page.jobcard.jobcard.execute",
		args:{
			'filters':from_date,
			'filters1':to_date
		},
		callback: function(r) {
				if (r.message) {
					$.each(r.message, function(i,d) {
						console.log(i.toString());
						console.log(d.toString());
						if (i == 0){
							columns = d;
						}else{
							data = d
						}

					});
					createSlickGridExtended('demo_div1', data, columns, options, additional_menu_entries);
				}
		}
	})
//'filters':'[frappe.datetime.add_months(frappe.datetime.get_today(),-1), frappe.datetime.get_today()]'






};
