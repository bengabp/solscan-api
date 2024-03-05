import React from "react";
import "../esin.css";
import { useNavigate, useNavigation, useParams } from "react-router-dom";
import { KeyboardArrowLeft as BackIcon } from "@mui/icons-material";

export default function DetailedPage() {
  // Page ID
  const { id } = useParams();
  const navigation = useNavigate();

  function goback() {
    navigation(-1);
  }

  return (
    <main className="bg-white mt-4">
      <div className="flex padding-1">
        <button onClick={goback} style={{}}>
          <div className="flex">
            <BackIcon />
          </div>
        </button>
      </div>
      <div>
        Lorem ipsum dolor sit amet consectetur adipisicing elit. Possimus,
        quibusdam similique consequuntur hic itaque deserunt amet rerum quo
        aperiam porro, eligendi quidem nobis nisi sequi, facilis officiis
        aspernatur? Quaerat eveniet illum, dolorum voluptatibus illo commodi
        modi eius, omnis cupiditate deserunt iusto, a atque maxime enim aliquid.
        Iusto eaque, id perspiciatis placeat necessitatibus odio explicabo iure
        ducimus aut neque voluptas reiciendis accusamus eos ipsam molestias.
        Facilis delectus, tempora eligendi quos eveniet accusamus eum amet
        itaque vitae obcaecati nulla cumque quisquam et quaerat necessitatibus
        excepturi provident, quibusdam non tenetur minus architecto dicta nobis
        neque. Totam quia, velit quibusdam sequi officiis perspiciatis
        repudiandae soluta ratione similique ab vitae, dolorem minima libero
        corporis rerum dignissimos eum non adipisci quasi pariatur illum
        architecto esse dolorum. Aut vitae tempore commodi modi, dignissimos
        velit eligendi, perspiciatis, porro harum quam culpa? Nulla earum,
        mollitia atque, vitae reiciendis possimus quos neque impedit, officiis
        voluptatibus sequi numquam ipsa aliquam ducimus. Quidem corporis veniam
        sed, facere fuga dicta eaque a praesentium, doloribus, ipsa illo
        exercitationem quos. Nihil reiciendis animi, iusto earum expedita
        exercitationem. Ducimus, maiores eaque quas ab placeat nostrum ipsum
        tenetur. Repellendus cum saepe vitae ab perferendis aliquid quia
        voluptatem qui ad quasi? Tempora inventore eaque odit aspernatur ut eum
        laudantium eius consequuntur accusantium iste vel sunt ullam quibusdam
        assumenda veniam, maxime nostrum ab officia voluptates eveniet fugiat.
        Tenetur id alias rem temporibus enim quasi maxime quo dolore qui? Rem
        esse quod id voluptatum veniam voluptatem modi quae eligendi cum magnam
        rerum consequatur reiciendis enim molestiae, soluta omnis quasi quaerat
        vero autem provident est similique eius ipsum ut! Doloribus optio
        eligendi autem amet! Laudantium eius qui praesentium voluptas odit
        repellendus quas pariatur blanditiis aspernatur commodi sint eveniet
        consectetur sequi alias veritatis dolores nemo minima placeat, quod
        dicta, animi odio voluptate, laborum ipsa. Blanditiis, corporis ducimus
        non porro molestiae iure commodi ut neque tempore optio earum unde
        accusamus minus dolorem cupiditate inventore adipisci, corrupti
        voluptatem? Necessitatibus saepe labore a unde commodi provident ea!
        Adipisci dicta eaque obcaecati reprehenderit aliquam rem quam, qui
        ducimus ipsa, consequatur ullam temporibus distinctio? Autem rem
        assumenda natus, quos aliquam maxime neque architecto. Aliquam facilis
        error dolore enim libero quo voluptatibus, nihil dolor iste explicabo
        fugiat nesciunt molestias similique perferendis consequuntur. Officia,
        voluptatem ad eveniet quibusdam excepturi molestias laudantium eaque
        adipisci aliquid. Nisi quae accusamus voluptates illum nobis, neque
        animi dolorem incidunt molestiae, quos aspernatur expedita maxime sed
        totam ducimus vel vero veritatis laudantium ipsa saepe dolores iusto
        illo voluptatibus rem. Corporis in nostrum harum nihil. Saepe rerum
        deserunt, ducimus molestias non odit. Excepturi voluptas ratione
        veritatis exercitationem iste consequuntur quis, voluptatem
        reprehenderit eaque rem quo vel sed eos nihil tempore nam doloremque
        natus quia ex facere nesciunt architecto inventore veniam! Soluta nihil
        animi debitis assumenda voluptas, sit doloremque sapiente hic voluptatem
        molestiae quam cum illum ipsam atque sed est iure fuga quod.
        Voluptatibus earum ipsam suscipit adipisci quaerat eius omnis illo porro
        odit, iure a unde asperiores natus fugiat consequatur soluta optio
        recusandae iste. Ab ullam, quas porro, recusandae cumque laboriosam
        beatae delectus eum culpa libero corporis fugit? Blanditiis magni hic
        fugit adipisci quidem deserunt corrupti maiores, consequuntur, quo velit
        laborum reiciendis, ullam nihil voluptate est. Nihil dolor, cum quis,
        porro quod mollitia adipisci voluptatem perferendis similique expedita
        atque? Placeat recusandae tenetur voluptatum velit saepe hic doloribus
        esse consequatur cum veniam alias ipsum, ratione neque fugiat nulla
        vitae quos laborum tempore eligendi quidem fuga consequuntur tempora
        vero nisi! Illo, doloribus quam adipisci delectus facere rerum. Sint
        minima ad laborum praesentium ex, voluptatum ea, alias voluptatibus modi
        dolorem minus id vitae? Asperiores nostrum expedita ab accusamus sint
        numquam, at dolorem tempore odio dignissimos, quae quasi nemo itaque
        sapiente pariatur, ad magni facilis sed nulla? Voluptate, assumenda
        perferendis libero repudiandae molestias dolorem quia laudantium non
        tenetur animi numquam voluptates consequuntur dolorum? Dolorum, vitae
        beatae aperiam nemo deleniti ratione? Tempore a atque cum? Recusandae
        error laboriosam eius facere officiis ut aut aperiam quibusdam eum vitae
        ab, praesentium est repudiandae? Aut reprehenderit modi totam distinctio
        hic recusandae unde. Alias cumque ad atque iste molestias placeat
        veniam, quaerat nam nesciunt aut explicabo distinctio labore maxime
        magnam pariatur, quasi obcaecati tenetur aspernatur soluta.
        Reprehenderit, repellat impedit! Voluptatum maxime cum magni voluptatem!
        Ipsa, velit cum? Consequuntur, id harum maiores, laborum provident neque
        impedit atque ipsum commodi ducimus veritatis eos minus enim! Inventore
        libero cum officia laudantium. Incidunt minima ad pariatur aliquam non
        eaque consectetur quis perspiciatis nostrum! Aliquid, molestiae?
        Molestiae, eum! Voluptatum corporis, sint hic maxime ex saepe debitis.
        Dicta deleniti quisquam cumque cupiditate architecto suscipit tempore
        vitae, harum at ducimus. Totam rem non error ad earum excepturi commodi,
        quia exercitationem debitis nesciunt dolores voluptatum omnis quas
        fugiat aut deserunt molestias vitae ipsum, architecto consequuntur
        repellendus minima consectetur at similique? Accusamus ducimus iure
        aspernatur? Magnam velit reiciendis nihil quas nulla alias unde,
        aspernatur cum ut laborum illo odio esse aut illum. Eum, illum vitae?
        Delectus error autem, sit eligendi ipsa facilis, dolorum eum ducimus
        repellat consectetur sed nostrum reiciendis. Quaerat nobis dolore harum.
        Reiciendis nostrum vero voluptas nulla ipsa, corporis ut facere eius est
        cum atque, et illum eaque eum quam architecto optio earum hic, itaque
        sunt? Maiores vitae quasi sunt unde porro alias qui, quibusdam at
        voluptates. Quod temporibus voluptatem nisi, minus, blanditiis quis
        accusamus nam modi sed quae veniam quisquam praesentium ipsa a iste
        voluptatibus odit sit voluptate. Molestias, accusantium perspiciatis?
        Nemo, pariatur error? Accusamus tempora alias maxime perspiciatis atque
        assumenda inventore facere? Quidem atque quasi fugit eaque. Facere sed
        quisquam consequuntur possimus vero. Ab natus voluptate, accusamus
        reiciendis, soluta suscipit quos quo architecto, labore libero ducimus
        dolorem. Architecto minima quo dolore quibusdam ducimus minus, eligendi
        molestiae! Incidunt iste, consectetur vel alias, at distinctio obcaecati
        eaque praesentium, animi quia nostrum consequatur reiciendis architecto
        a fugiat excepturi ipsa ratione molestias vero nobis. Odio magnam esse
        nemo, in aliquid nulla. Officia ad, ut dolorum corrupti inventore
        eveniet doloribus pariatur laborum est perspiciatis quisquam dignissimos
        quae commodi fugit ab rem nam labore, dolore totam eum magni
        repudiandae? Dolore tempora reiciendis, eius porro numquam laudantium
        delectus, aut facere sapiente nam ullam, voluptas aspernatur!
        Asperiores, nisi.
      </div>
    </main>
  );
}
