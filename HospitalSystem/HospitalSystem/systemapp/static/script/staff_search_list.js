var as = document.querySelectorAll("#results>a");
for(var a in as) {
    if (a.class === "appiontment_link") {
        a.onclick(function render() {
            var span_id = document.querySelector("a>span");
            var id = span_id.value;
            $.post("/check_appointment", {
                "id": id
            })
        });
    }
}