var CSSImportModule = function() {
    this.render = function() {
        var seed = document.getElementById("seed_id");

        seed.style.display = "inline-block";
        seed.style.width = "210px";
        seed.type = "input";
    };

    this.reset = function() {
        console.log("reset");
    };
}
