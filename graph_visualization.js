import {
  Runtime,
  Inspector,
} from "https://cdn.jsdelivr.net/npm/@observablehq/runtime@4/dist/runtime.js";

function hideElement(id) {
  document.getElementById(id).style.display = "none";
}

function showElement(id) {
  document.getElementById(id).style.display = "block";
}

export async function createElementsFromDataUrls(data_urls) {
  async function doDisplay(nameToDisplay) {
    for (let name of Object.keys(await data_urls)) {
      hideElement(`${name}-graph`);
    }
    showElement(`${nameToDisplay}-graph`);
  }

  for (let [name, url] of Object.entries(await data_urls)) {
    url = `./data/for_visualization/${url}`;

    const button = document.createElement("button");
    const graph = document.createElement("div");
    const sizeSlider = document.createElement("div");

    button.setAttribute("id", `${name}-button`);
    button.innerText = `${name}`;
    button.onclick = () => doDisplay(`${name}`);
    document.getElementById("button-container").appendChild(button);

    sizeSlider.classList.add("size-slider");
    sizeSlider.innerHTML = `<input type="range" id="${name}-node-size-slider" name="granularity" min="0" max="100" value="10" step="10"> Granularity (ignore nodes and links smaller than) </input>`;
    sizeSlider.oninput = () => {
      graph.innerHTML = "";
      graph.appendChild(sizeSlider);
      createGraphElement(url, name);
    };

    graph.appendChild(sizeSlider);
    graph.setAttribute("id", `${name}-graph`);
    graph.setAttribute("class", `graph`);
    document.getElementById("graph-container").appendChild(graph);
    createGraphElement(url, name);
  }

  doDisplay(Object.keys(await data_urls)[0]);
}

function createGraphElement(data_url, name) {
  buildGraphFromNodesLinks(data_url);
  const inspect = Inspector.into(`#${name}-graph`);
  new Runtime().module(
    buildGraphFromNodesLinks(data_url, name),
    (name) => name === "chart" && inspect()
  );
}

function buildGraphFromNodesLinks(data_url, name) {
  function define(runtime, observer) {
    const main = runtime.module();
    main
      .variable(observer("chart"))
      .define(
        "chart",
        ["data", "d3", "width", "height", "color", "drag", "invalidation"],
        function (data, d3, width, height, color, drag, invalidation) {
          const min_node_popularity = document.getElementById(
            `${name}-node-size-slider`
          ).value;
          const min_link_value = document.getElementById(
            `${name}-node-size-slider`
          ).value;

          const nodes = data.items.nodes
            .filter((node) => node.popularity > min_node_popularity)
            .map((d) => Object.create(d));
          const links = data.items.links
            .filter((link) => link.value > min_link_value)
            .map((d) => Object.create(d));

          const simulation = d3
            .forceSimulation(nodes)
            .force(
              "link",
              d3.forceLink(links).id((d) => d.id)
            )
            .force(
              "charge",
              d3.forceManyBody().strength((d) => -50 * Math.sqrt(d.popularity))
            )
            .force("center", d3.forceCenter(width / 2, height / 2));

          const svg = d3.create("svg").attr("viewBox", [0, 0, width, height]);

          const link = svg
            .append("g")
            .attr("stroke", "#999")
            .selectAll("line")
            .data(links)
            .join("line")
            .attr("stroke-opacity", (d) => 0.2)
            .attr("stroke-width", (d) => d.value * 0.1);

          const node = svg
            .append("g")
            .attr("class", "nodes")
            .attr("stroke", "#fff")
            .attr("stroke-width", 0.1)
            .selectAll("circle")
            .data(nodes)
            .join("circle")
            .attr("r", (d) => Math.sqrt(d.popularity) * 2)
            .attr("fill", color)
            .call(drag(simulation));

          node
            .append("title")
            .text((d) => d.id + ": " + d.popularity + " mentions");

          const text = svg
            .selectAll("nodes")
            .data(nodes)
            .join("text")
            .attr("x", (d, i) => i * 15)
            .attr("y", 17)
            .attr("dy", "0.2em")
            .attr("font-family", "Verdana")
            .attr("font-size", (d) => Math.pow(d.popularity, 1 / 6) * 5)
            .text((d) => d.id);

          simulation.on("tick", () => {
            link
              .attr("x1", (d) => d.source.x)
              .attr("y1", (d) => d.source.y)
              .attr("x2", (d) => d.target.x)
              .attr("y2", (d) => d.target.y);

            node.attr("cx", (d) => d.x).attr("cy", (d) => d.y);

            text
              .attr("x", (d) => d.x) //position of the lower left point of the text
              .attr("y", (d) => d.y); //position of the lower left point of the text
          });

          invalidation.then(() => simulation.stop());

          return svg.node();
        }
      );
    main.variable(observer("data")).define("data", function () {
      return fetch(data_url).then((res) => res.json());
    });
    main.variable(observer("height")).define("height", function () {
      return 900;
    });
    main.variable(observer("color")).define("color", ["d3"], function (d3) {
      const scale = d3.scaleOrdinal(
        [4, 3, 2, 1, 0],
        [`orange`, `lightgreen`, `cyan`, `khaki`, `lightgrey`]
      );
      // d3.schemeSet2
      return (d) => scale(parseInt((Math.sqrt(d.popularity) / 25) * 5));
    });
    main.variable(observer("drag")).define("drag", ["d3"], function (d3) {
      return (simulation) => {
        function dragstarted(d) {
          if (!d3.event.active) simulation.alphaTarget(0.3).restart();
          d.fx = d.x;
          d.fy = d.y;
        }

        function dragged(d) {
          d.fx = d3.event.x;
          d.fy = d3.event.y;
        }

        function dragended(d) {
          if (!d3.event.active) simulation.alphaTarget(0);
          d.fx = null;
          d.fy = null;
        }

        return d3
          .drag()
          .on("start", dragstarted)
          .on("drag", dragged)
          .on("end", dragended);
      };
    });
    main.variable(observer("d3")).define("d3", ["require"], function (require) {
      return require("d3@5");
    });
    return main;
  }

  return define;
}
