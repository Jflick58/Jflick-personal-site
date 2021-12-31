import * as React from "react"
import { Link } from "gatsby"
import { StaticImage } from "gatsby-plugin-image"

import Layout from "../components/layout"
import Seo from "../components/seo"
import PostsList from '../components/postsList';

const AboutPage = () => (
  <Layout>
    <Seo title="About" />
    <div class="split">
      <div class="left">
        <h1>Welcome. <span class="emphasis">I'm Justin.</span></h1>
        <h2>About Me </h2>
        <p>I find myself to be a passionately curious person. I love to learn about new things, and whether it be data approaches, drum fills, or BBQ techniques, you'll often find me down a rabbit hole, trying to learn as much as I possibly can about the thing I'm trying to figure out at the time. I'm constantly reading and trying to both deepend and broaden my knowledge in various areas of Computer Science. I'm also extremely fascinated by organizational dynamics, espeically in technical organizations, and it's a topic I plan on writing about a bit in my blog.</p>
        <p> When I write code, I'm typically reaching for Python, but I've utilized a variety of other languages. I like to tinker, so I'm often trying to to learn new languages and frameworks. In my professional time, I focus on Data Engineering and backend development, so that tends to keep me in Python. Although as I spend more time in management roles, the percentage of time I'm hands-on-keyboard drops, so I'll reach for familar tools when I'm trying to get things done quickly. </p>
    <h2>Career and Education</h2>
    <img class="company-logo" src="https://1000logos.net/wp-content/uploads/2020/06/KPMG-Logo.png"></img>
    <p>I finished my Bachelor of Science Degree in Management Information Systems at Calfornia State University, Chico. I then joined KPMG as an Advisory Associate in their State and Local Government practice where I had the opportunity to work on large data integration efforts for various state government agencies, most notably the State of Hawaii <a href="https://medical.mybenefits.hawaii.gov/web/kolea/home-page">KOLEA</a> medicaid eligibity system, and the State of Ohio <a href="https://das.ohio.gov/Divisions/General-Services/Procurement-Services/Ohio-Buys#5223482-home">eProcurement</a> System. </p>
    <img class="company-logo" src="https://i0.wp.com/www.engage3.com/wp-content/uploads/2019/07/engage3_logo.png?fit=1107%2C264&ssl=1"></img>
    <p>I then transitioned to <a href="https://www.engage3.com">Engage3</a>, a retail price optimization startup where I lead a Data Engineering team responsible for collecting and managing data on billions of retail products across the largest retailers in the world. It was in this role that I honed my ability to build highly flexible data systems that could accomdate the explosive growth that we experienced.</p>
    <img class="company-logo" src="https://www.investopedia.com/thmb/QzV0NnWgLneRsAJN33sQQBDfdLo=/3000x596/filters:no_upscale()/homesite-insurance-logo-9d474e36c3104661a0e89ef8e5208be4.png"></img>
    <p>In early 2021, it was time for my next challenge. I jumped to <a href="https://go.homesite.com">Homesite Insurance</a> where I now lead a team of experienced Data Engineers and Architects building the next generation of Data Engineering as we make the transition to a cloud-native, highly scable data architecture. I'm also heavily involved with taking Data Science models into production in both a project management and hands-on capacity. </p>
    <img class="company-logo" src=" https://brand.gatech.edu/sites/default/files/inline-images/extended-RGB.png"></img>
   <p>I've also been pursuing my Master's in Computer Science at Georgia Institute of Technology, where I have elected to specalize in Machine Learning. As I have been working full-time in addition to my studies, I'm currently projected to grauate at the end of 2022. </p>
      </div>
      {/* <div class="right">
        <img class="profile-pic" src="https://avatars.githubusercontent.com/u/22459070?v=4"></img> */}
        {/* <h2 style={{"text-align": "center"}}>Employment</h2>
        <div class="three-split">
          <div class="three-split-left">
            <img class="company-logo" src="https://1000logos.net/wp-content/uploads/2020/06/KPMG-Logo.png"></img>
          </div>
          <div class="three-split-middle">
            <img class="company-logo" src="https://i0.wp.com/www.engage3.com/wp-content/uploads/2019/07/engage3_logo.png?fit=1107%2C264&ssl=1"></img>
          </div>
          <div class="three-split-right">
            <img class="company-logo" src="https://www.investopedia.com/thmb/QzV0NnWgLneRsAJN33sQQBDfdLo=/3000x596/filters:no_upscale()/homesite-insurance-logo-9d474e36c3104661a0e89ef8e5208be4.png"></img>
          </div>
        </div> */}
      {/* </div> */}
    </div>
  </Layout>
)

export default AboutPage
